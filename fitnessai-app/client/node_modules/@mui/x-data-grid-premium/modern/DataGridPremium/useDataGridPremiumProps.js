import _objectWithoutPropertiesLoose from "@babel/runtime/helpers/esm/objectWithoutPropertiesLoose";
import _extends from "@babel/runtime/helpers/esm/extends";
const _excluded = ["components", "componentsProps"];
import * as React from 'react';
import { useThemeProps } from '@mui/material/styles';
import { DATA_GRID_PRO_PROPS_DEFAULT_VALUES, GRID_DEFAULT_LOCALE_TEXT } from '@mui/x-data-grid-pro';
import { computeSlots, uncapitalizeObjectKeys } from '@mui/x-data-grid-pro/internals';
import { GRID_AGGREGATION_FUNCTIONS } from '../hooks/features/aggregation';
import { DATA_GRID_PREMIUM_DEFAULT_SLOTS_COMPONENTS } from '../constants/dataGridPremiumDefaultSlotsComponents';

/**
 * The default values of `DataGridPremiumPropsWithDefaultValue` to inject in the props of DataGridPremium.
 */
export const DATA_GRID_PREMIUM_PROPS_DEFAULT_VALUES = _extends({}, DATA_GRID_PRO_PROPS_DEFAULT_VALUES, {
  unstable_cellSelection: false,
  disableAggregation: false,
  disableRowGrouping: false,
  rowGroupingColumnMode: 'single',
  aggregationFunctions: GRID_AGGREGATION_FUNCTIONS,
  aggregationRowsScope: 'filtered',
  getAggregationPosition: groupNode => groupNode.depth === -1 ? 'footer' : 'inline'
});
const defaultSlots = uncapitalizeObjectKeys(DATA_GRID_PREMIUM_DEFAULT_SLOTS_COMPONENTS);
export const useDataGridPremiumProps = inProps => {
  const _useThemeProps = useThemeProps({
      props: inProps,
      name: 'MuiDataGrid'
    }),
    {
      components,
      componentsProps
    } = _useThemeProps,
    themedProps = _objectWithoutPropertiesLoose(_useThemeProps, _excluded);
  const localeText = React.useMemo(() => _extends({}, GRID_DEFAULT_LOCALE_TEXT, themedProps.localeText), [themedProps.localeText]);
  const slots = React.useMemo(() => computeSlots({
    defaultSlots,
    components,
    slots: themedProps.slots
  }), [components, themedProps.slots]);
  return React.useMemo(() => _extends({}, DATA_GRID_PREMIUM_PROPS_DEFAULT_VALUES, themedProps, {
    slotProps: themedProps.slotProps ?? componentsProps,
    localeText,
    slots,
    signature: 'DataGridPremium'
  }), [themedProps, componentsProps, localeText, slots]);
};