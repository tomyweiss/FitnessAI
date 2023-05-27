import _objectWithoutProperties from "@babel/runtime/helpers/esm/objectWithoutProperties";
import _extends from "@babel/runtime/helpers/esm/extends";
var _excluded = ["components", "componentsProps"];
import * as React from 'react';
import { useThemeProps } from '@mui/material/styles';
import { GRID_DEFAULT_LOCALE_TEXT, DATA_GRID_PROPS_DEFAULT_VALUES } from '@mui/x-data-grid';
import { computeSlots, uncapitalizeObjectKeys } from '@mui/x-data-grid/internals';
import { DATA_GRID_PRO_DEFAULT_SLOTS_COMPONENTS } from '../constants/dataGridProDefaultSlotsComponents';

/**
 * The default values of `DataGridProPropsWithDefaultValue` to inject in the props of DataGridPro.
 */
export var DATA_GRID_PRO_PROPS_DEFAULT_VALUES = _extends({}, DATA_GRID_PROPS_DEFAULT_VALUES, {
  scrollEndThreshold: 80,
  treeData: false,
  defaultGroupingExpansionDepth: 0,
  disableColumnPinning: false,
  keepColumnPositionIfDraggedOutside: false,
  disableChildrenFiltering: false,
  disableChildrenSorting: false,
  rowReordering: false,
  rowsLoadingMode: 'client',
  getDetailPanelHeight: function getDetailPanelHeight() {
    return 500;
  }
});
var defaultSlots = uncapitalizeObjectKeys(DATA_GRID_PRO_DEFAULT_SLOTS_COMPONENTS);
export var useDataGridProProps = function useDataGridProProps(inProps) {
  var _useThemeProps = useThemeProps({
      props: inProps,
      name: 'MuiDataGrid'
    }),
    components = _useThemeProps.components,
    componentsProps = _useThemeProps.componentsProps,
    themedProps = _objectWithoutProperties(_useThemeProps, _excluded);
  var localeText = React.useMemo(function () {
    return _extends({}, GRID_DEFAULT_LOCALE_TEXT, themedProps.localeText);
  }, [themedProps.localeText]);
  var slots = React.useMemo(function () {
    return computeSlots({
      defaultSlots: defaultSlots,
      slots: themedProps.slots,
      components: components
    });
  }, [components, themedProps.slots]);
  return React.useMemo(function () {
    var _themedProps$slotProp;
    return _extends({}, DATA_GRID_PRO_PROPS_DEFAULT_VALUES, themedProps, {
      localeText: localeText,
      slots: slots,
      slotProps: (_themedProps$slotProp = themedProps.slotProps) != null ? _themedProps$slotProp : componentsProps,
      signature: 'DataGridPro'
    });
  }, [themedProps, localeText, slots, componentsProps]);
};