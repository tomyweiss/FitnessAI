import { passFilterLogic } from '@mui/x-data-grid/internals';
export const TREE_DATA_STRATEGY = 'tree-data';

/**
 * A node is visible if one of the following criteria is met:
 * - One of its children is passing the filter
 * - It is passing the filter
 */
export const filterRowTreeFromTreeData = params => {
  const {
    rowTree,
    disableChildrenFiltering,
    isRowMatchingFilters
  } = params;
  const visibleRowsLookup = {};
  const filteredRowsLookup = {};
  const filteredDescendantCountLookup = {};
  const filterTreeNode = (node, isParentMatchingFilters, areAncestorsExpanded) => {
    const shouldSkipFilters = disableChildrenFiltering && node.depth > 0;
    let isMatchingFilters;
    if (shouldSkipFilters) {
      isMatchingFilters = null;
    } else if (!isRowMatchingFilters || node.type === 'footer') {
      isMatchingFilters = true;
    } else {
      const {
        passingFilterItems,
        passingQuickFilterValues
      } = isRowMatchingFilters(node.id);
      isMatchingFilters = passFilterLogic([passingFilterItems], [passingQuickFilterValues], params.filterModel, params.apiRef);
    }
    let filteredDescendantCount = 0;
    if (node.type === 'group') {
      node.children.forEach(childId => {
        const childNode = rowTree[childId];
        const childSubTreeSize = filterTreeNode(childNode, isMatchingFilters ?? isParentMatchingFilters, areAncestorsExpanded && !!node.childrenExpanded);
        filteredDescendantCount += childSubTreeSize;
      });
    }
    let shouldPassFilters;
    switch (isMatchingFilters) {
      case true:
        {
          shouldPassFilters = true;
          break;
        }
      case false:
        {
          shouldPassFilters = filteredDescendantCount > 0;
          break;
        }
      default:
        {
          shouldPassFilters = isParentMatchingFilters;
          break;
        }
    }
    visibleRowsLookup[node.id] = shouldPassFilters && areAncestorsExpanded;
    filteredRowsLookup[node.id] = shouldPassFilters;

    // TODO: Should we keep storing the visibility status of footer independently or rely on the group visibility in the selector ?
    if (node.type === 'group' && node.footerId != null) {
      visibleRowsLookup[node.footerId] = shouldPassFilters && areAncestorsExpanded && !!node.childrenExpanded;
    }
    if (!shouldPassFilters) {
      return 0;
    }
    filteredDescendantCountLookup[node.id] = filteredDescendantCount;
    if (node.type === 'footer') {
      return filteredDescendantCount;
    }
    return filteredDescendantCount + 1;
  };
  const nodes = Object.values(rowTree);
  for (let i = 0; i < nodes.length; i += 1) {
    const node = nodes[i];
    if (node.depth === 0) {
      filterTreeNode(node, true, true);
    }
  }
  return {
    visibleRowsLookup,
    filteredRowsLookup,
    filteredDescendantCountLookup
  };
};