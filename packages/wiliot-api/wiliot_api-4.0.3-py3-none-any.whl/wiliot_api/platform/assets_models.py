from sgqlc.types.datetime import Date
from sgqlc.types import String, Float, Type, Int, list_of, Field, Boolean
from sgqlc.types.relay import Node, Connection
from sgqlc.operation import Operation


class Tag(Type):
    tagId = String


class Category(Type):
    id = String
    name = String


class AssetNode(Type):
    id = String
    name = String
    tags = Field(Tag)
    createdAt = Int
    createdBy = String
    lastUpdatedBy = String
    lastUpdatedAt = String
    tagId = String
    status = String
    poiId = String
    categoryId = String
    category = Field(Category)


class PageInfoNode(Type):
    cursor = String
    hasNext = Boolean
    totalPages = Int


class AssetConnection(Type):
    page = list_of(AssetNode)
    pageInfo = Field(PageInfoNode)


class StringFilter(Type):
    filterType = String
    value = String

    def __to_graphql_input__(self, value, indent, indent_string="\t"):
        return f"{{{self.filterType}: \"{self.value}\"}}"


class Query(Type):
    assets = Field(AssetConnection, args={
        'pageSize': Int,
        'cursor': String,
        'categoryId': StringFilter
    })