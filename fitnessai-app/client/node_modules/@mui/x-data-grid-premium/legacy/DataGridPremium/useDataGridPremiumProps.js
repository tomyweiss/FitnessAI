import _objectWithoutProperties from "@babel/runtime/helpers/esm/objectWithoutProperties";
import _extends from "@babel/runtime/helpers/esm/extends";
var _excluded = ["components", "componentsProps"];
import * as React from 'react';
import { useThemeProps } from '@mui/material/styles';
import { DATA_GRID_PRO_PROPS_DEFAULT_VALUES, GRID_DEFAULT_LOCALE_TEXT } from '@mui/x-data-grid-pro';
import { computeSlots, uncapitalizeObjectKeys } from '@mui/x-data-grid-pro/internals';
import { GRID_AGGREGATION_FUNCTIONS } from '../hooks/features/aggregation';
import { DATA_GRID_PREMIUM_DEFAULT_SLOTS_COMPONENTS } from '../constants/dataGridPremiumDefaultSlotsComponents';

/**
 * The default values of `DataGridPremiumPropsWithDefaultValue` to inject in the props of DataGridPremium.
 */
export var DATA_GRID_PREMIUM_PROPS_DEFAULT_VALUES = _extends({}, DATA_GRID_PRO_PROPS_DEFAULT_VALUES, {
  unstable_cellSelection: false,
  disableAggregation: false,
  disableRowGrouping: false,
  rowGroupingColumnMode: 'single',
  aggregationFunctions: GRID_AGGREGATION_FUNCTIONS,
  aggregationRowsScope: 'filtered',
  getAggregationPosition: function getAggregationPosition(groupNode) {
    return groupNode.depth === -1 ? 'footer' : 'inline';
  }
});
var defaultSlots = uncapitalizeObjectKeys(DATA_GRID_PREMIUM_DEFAULT_SLOTS_COMPONENTS);
export var useDataGridPremiumProps = function useDataGridPremiumProps(inProps) {
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
      components: components,
      slots: themedProps.slots
    });
  }, [components, themedProps.slots]);
  return React.useMemo(function () {
    var _themedProps$slotProp;
    return _extends({}, DATA_GRID_PREMIUM_PROPS_DEFAULT_VALUES, themedProps, {
      slotProps: (_themedProps$slotProp = themedProps.slotProps) != null ? _themedProps$slotProp : componentsProps,
      localeText: localeText,
      slots: slots,
      signature: 'DataGridPremium'
    });
  }, [themedProps, componentsProps, localeText, slots]);
};