import _toConsumableArray from "@babel/runtime/helpers/esm/toConsumableArray";
import { GRID_ROOT_GROUP_ID } from '@mui/x-data-grid';
export var sortRowTree = function sortRowTree(params) {
  var rowTree = params.rowTree,
    disableChildrenSorting = params.disableChildrenSorting,
    sortRowList = params.sortRowList,
    shouldRenderGroupBelowLeaves = params.shouldRenderGroupBelowLeaves;
  var sortedRows = [];
  var sortedGroupedByParentRows = new Map();
  var sortGroup = function sortGroup(node) {
    var shouldSortGroup = !!sortRowList && (!disableChildrenSorting || node.depth === -1);
    var sortedRowIds;
    if (shouldSortGroup) {
      for (var i = 0; i < node.children.length; i += 1) {
        var childNode = rowTree[node.children[i]];
        if (childNode.type === 'group') {
          sortGroup(childNode);
        }
      }
      sortedRowIds = sortRowList(node.children.map(function (childId) {
        return rowTree[childId];
      }));
    } else if (shouldRenderGroupBelowLeaves) {
      var childrenLeaves = [];
      var childrenGroups = [];
      for (var _i = 0; _i < node.children.length; _i += 1) {
        var childId = node.children[_i];
        var _childNode = rowTree[childId];
        if (_childNode.type === 'group') {
          sortGroup(_childNode);
          childrenGroups.push(childId);
        } else if (_childNode.type === 'leaf') {
          childrenLeaves.push(childId);
        }
      }
      sortedRowIds = [].concat(childrenLeaves, childrenGroups);
    } else {
      for (var _i2 = 0; _i2 < node.children.length; _i2 += 1) {
        var _childNode2 = rowTree[node.children[_i2]];
        if (_childNode2.type === 'group') {
          sortGroup(_childNode2);
        }
      }
      sortedRowIds = _toConsumableArray(node.children);
    }
    if (node.footerId != null) {
      sortedRowIds.push(node.footerId);
    }
    sortedGroupedByParentRows.set(node.id, sortedRowIds);
  };
  sortGroup(rowTree[GRID_ROOT_GROUP_ID]);

  // Flatten the sorted lists to have children just after their parent
  var insertRowListIntoSortedRows = function insertRowListIntoSortedRows(startIndex, rowList) {
    sortedRows = [].concat(_toConsumableArray(sortedRows.slice(0, startIndex)), _toConsumableArray(rowList), _toConsumableArray(sortedRows.slice(startIndex)));
    var treeSize = 0;
    rowList.forEach(function (rowId) {
      treeSize += 1;
      var children = sortedGroupedByParentRows.get(rowId);
      if (children != null && children.length) {
        var subTreeSize = insertRowListIntoSortedRows(startIndex + treeSize, children);
        treeSize += subTreeSize;
      }
    });
    return treeSize;
  };
  insertRowListIntoSortedRows(0, sortedGroupedByParentRows.get(GRID_ROOT_GROUP_ID));
  return sortedRows;
};