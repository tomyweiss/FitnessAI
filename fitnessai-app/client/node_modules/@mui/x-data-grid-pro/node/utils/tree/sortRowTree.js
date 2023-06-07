"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.sortRowTree = void 0;
var _xDataGrid = require("@mui/x-data-grid");
const sortRowTree = params => {
  const {
    rowTree,
    disableChildrenSorting,
    sortRowList,
    shouldRenderGroupBelowLeaves
  } = params;
  let sortedRows = [];
  const sortedGroupedByParentRows = new Map();
  const sortGroup = node => {
    const shouldSortGroup = !!sortRowList && (!disableChildrenSorting || node.depth === -1);
    let sortedRowIds;
    if (shouldSortGroup) {
      for (let i = 0; i < node.children.length; i += 1) {
        const childNode = rowTree[node.children[i]];
        if (childNode.type === 'group') {
          sortGroup(childNode);
        }
      }
      sortedRowIds = sortRowList(node.children.map(childId => rowTree[childId]));
    } else if (shouldRenderGroupBelowLeaves) {
      const childrenLeaves = [];
      const childrenGroups = [];
      for (let i = 0; i < node.children.length; i += 1) {
        const childId = node.children[i];
        const childNode = rowTree[childId];
        if (childNode.type === 'group') {
          sortGroup(childNode);
          childrenGroups.push(childId);
        } else if (childNode.type === 'leaf') {
          childrenLeaves.push(childId);
        }
      }
      sortedRowIds = [...childrenLeaves, ...childrenGroups];
    } else {
      for (let i = 0; i < node.children.length; i += 1) {
        const childNode = rowTree[node.children[i]];
        if (childNode.type === 'group') {
          sortGroup(childNode);
        }
      }
      sortedRowIds = [...node.children];
    }
    if (node.footerId != null) {
      sortedRowIds.push(node.footerId);
    }
    sortedGroupedByParentRows.set(node.id, sortedRowIds);
  };
  sortGroup(rowTree[_xDataGrid.GRID_ROOT_GROUP_ID]);

  // Flatten the sorted lists to have children just after their parent
  const insertRowListIntoSortedRows = (startIndex, rowList) => {
    sortedRows = [...sortedRows.slice(0, startIndex), ...rowList, ...sortedRows.slice(startIndex)];
    let treeSize = 0;
    rowList.forEach(rowId => {
      treeSize += 1;
      const children = sortedGroupedByParentRows.get(rowId);
      if (children?.length) {
        const subTreeSize = insertRowListIntoSortedRows(startIndex + treeSize, children);
        treeSize += subTreeSize;
      }
    });
    return treeSize;
  };
  insertRowListIntoSortedRows(0, sortedGroupedByParentRows.get(_xDataGrid.GRID_ROOT_GROUP_ID));
  return sortedRows;
};
exports.sortRowTree = sortRowTree;