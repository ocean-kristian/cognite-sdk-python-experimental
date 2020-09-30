from collections import defaultdict, namedtuple
from typing import Any, Dict, Generator, List, Union

from cognite.client import utils
from cognite.client.beta import CogniteClient
from cognite.client.data_classes import Asset, Event, Relationship, Sequence, TimeSeries
from cognite.client.data_classes._base import CogniteResource
from cognite.client.data_classes.files import FileMetadata
from cognite.client.data_classes.labels import LabelFilter

ResourceRef = namedtuple("ResourceRef", ["type", "external_id"])
Resource = Union[Asset, TimeSeries, Event, FileMetadata, Sequence]


class RelationshipFilterBase:
    def is_inside(self, resource: Resource) -> bool:
        return False


class RelationshipFilter(RelationshipFilterBase):
    def __init__(self, labels):
        self.labels = labels

    def is_inside(self, resource: Resource):
        if resource.labels is not None:
            labels_decoded = [label["externalId"] for label in resource.labels]
            return any(label in self.labels for label in labels_decoded)
        else:
            return False


class RelationshipFilterAll(RelationshipFilterBase):
    def is_inside(self, resource: Resource):
        return True


class RelationshipWithResource(CogniteResource):
    def __init__(self, relationship: Relationship, source_resource: Resource, target_resource: Resource):
        self.relationship = relationship
        self.source_resource = source_resource
        self.target_resource = target_resource


class Fetcher:
    def __init__(self, has_ignore_unknown_ids, retrieve_multiple):
        self.has_ignore_unknown_ids = has_ignore_unknown_ids
        self.retrieve_multiple = retrieve_multiple

    def retrieve_multiple(self, external_ids: List[str]):
        if self.has_ignore_unknown_ids:
            return self.retrieve_multiple(external_ids=external_ids, ignore_unknown_ids=True)
        else:
            return self.retrieve_multiple(external_ids=external_ids)


class RelationshipsQuery:
    def __init__(self, client: CogniteClient):
        self.client = client
        self.fetchers = {
            "asset": Fetcher(True, self.client.assets.retrieve_multiple),
            "timeSeries": Fetcher(True, self.client.time_series.retrieve_multiple),
            "file": Fetcher(False, self.client.files.retrieve_multiple),
            "event": Fetcher(True, self.client.events.retrieve_multiple),
            "sequence": Fetcher(False, self.client.sequences.retrieve_multiple),
        }

    def query(
        self,
        sources: List[Resource] = None,
        source_types: List[str] = None,
        sources_filter: RelationshipFilter = None,
        targets: List[Resource] = None,
        target_types: List[str] = None,
        targets_filter: RelationshipFilter = None,
        data_set_ids: List[Dict[str, Any]] = None,
        labels: LabelFilter = None,
        limit: int = None,
    ) -> Generator[RelationshipWithResource, None, None]:
        """Query relationships and resolve referenced resources in one go.

        Args:
            sources (List[Resource]): Return only the relationships matching one of these resources as the source of a relationship
            source_types (List[str]): Include relationships that have any of these values in their source Type field
            sources_filter: RelationshipFilter: Filter source resources by their label
            targets (List[Resource]): Return only the relationships matching one of these resources as the target of a relationship
            target_types (List[str]): Include relationships that have any of these values in their target Type field
            targets_filter: RelationshipFilter: Filter target resources by their label
            data_set_ids (List[Dict[str, Any]]): Either one of internalId (int) or externalId (str)
            labels (LabelFilter): Return only the resource matching the specified label constraint
            limit (int): Maximum number of relationships to return. Defaults to 100. Set to -1, float("inf") or None
                to return all items.

        Returns:
            Generator[RelationshipWithResource, None, None]: Generator of requested relationships where each relationship also has 'source_resource' and 'target_resource'.

        Examples:

            List relationships::

                >>> from cognite.client.beta import CogniteClient
                >>> from cognite.experimental import RelationshipsQuery
                >>> c = CogniteClient()
                >>> rel_query = RelationshipsQuery(c)
                >>> rel_query.query()

            Filter relationships by target node label::

                >>> from cognite.client.beta import CogniteClient
                >>> from cognite.experimental import RelationshipsQuery
                >>> c = CogniteClient()
                >>> rel_query = RelationshipsQuery(c)
                >>> rel_query.query(targets_filter=RelationshipFilter(labels = ["Pump", "Valve"]))

            Filter relationships by sources::

                >>> from cognite.client.beta import CogniteClient
                >>> from cognite.experimental import RelationshipsQuery
                >>> c = CogniteClient()
                >>> rel_query = RelationshipsQuery(c)
                >>> sources = c.assets.list()
                >>> rel_query.query(sources=sources)

            Use result of a query::

                >>> from cognite.client.beta import CogniteClient
                >>> from cognite.experimental import RelationshipsQuery
                >>> c = CogniteClient()
                >>> rel_query = RelationshipsQuery(c)
                >>> result = rel_query.query()
                >>> for res in result:
                >>>     print(res.source_resource.name, res.target_resource.name)
        """
        sources_filter = sources_filter if sources_filter is not None else RelationshipFilterAll()
        targets_filter = targets_filter if targets_filter is not None else RelationshipFilterAll()

        relations = self.client.relationships.list(
            source_external_ids=set([res.external_id for res in sources]) if sources is not None else None,
            source_types=source_types,
            target_external_ids=set([res.external_id for res in targets]) if targets is not None else None,
            target_types=target_types,
            labels=labels,
            data_set_ids=data_set_ids,
            limit=limit,
        )

        resource_refs = set(
            [ResourceRef(type=rel.source_type, external_id=rel.source_external_id) for rel in relations]
            + [ResourceRef(type=rel.target_type, external_id=rel.target_external_id) for rel in relations]
        )

        resources_by_type = defaultdict(list)
        for res in resource_refs:
            resources_by_type[res.type].append(res.external_id)

        def fetch_per_type(type, external_ids):
            resources = self.fetchers[type].retrieve_multiple(external_ids=external_ids)
            return [(type, res) for res in resources]

        tasks_summary = utils._concurrency.execute_tasks_concurrently(
            fetch_per_type, [(type, external_ids) for type, external_ids in resources_by_type.items()], max_workers=5
        )

        if tasks_summary.exceptions:
            raise tasks_summary.exceptions[0]

        resources_by_ext_id = {}
        for item in tasks_summary.joined_results():
            type, res = item
            resources_by_ext_id[ResourceRef(type, res.external_id)] = res

        for rel in relations:
            source_ref = ResourceRef(rel.source_type, rel.source_external_id)
            source_resource = resources_by_ext_id.get(source_ref)
            target_ref = ResourceRef(rel.target_type, rel.target_external_id)
            target_resource = resources_by_ext_id.get(target_ref)
            if (
                source_resource is not None
                and sources_filter.is_inside(source_resource)
                and target_resource is not None
                and targets_filter.is_inside(target_resource)
            ):
                yield RelationshipWithResource(rel, source_resource, target_resource)
