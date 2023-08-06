/**
 * Copyright (c) 2021- Equinor ASA
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import React from "react";
import PropTypes, { InferProps } from "prop-types";
import { default as ReactSelect } from "react-select";
import {
    components,
    OptionProps,
    MultiValueProps,
    ValueContainerProps,
} from "react-select";

import {
    getPropsWithMissingValuesSetToDefault,
    Optionals,
} from "../Utils/DefaultPropsHelpers";

const propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string.isRequired,
    /**
     * The value of the input. If `multi` is false
     * then value is just a string that corresponds to the values
     * provided in the `options` property. If `multi` is true, then
     * multiple values can be selected at once, and `value` is an
     * array of items with values corresponding to those in the
     * `options` prop.
     */
    value: PropTypes.oneOfType([
        PropTypes.string.isRequired,
        PropTypes.number.isRequired,
        PropTypes.arrayOf(
            PropTypes.oneOfType([
                PropTypes.string.isRequired,
                PropTypes.number.isRequired,
            ]).isRequired
        ).isRequired,
        PropTypes.arrayOf(
            PropTypes.exact({
                label: PropTypes.oneOfType([
                    PropTypes.string.isRequired,
                    PropTypes.number.isRequired,
                ]).isRequired,
                value: PropTypes.oneOfType([
                    PropTypes.string.isRequired,
                    PropTypes.number.isRequired,
                ]).isRequired,
            }).isRequired
        ),
    ]),
    /**
     * An array of options {label: [string|number], value: [string|number]},
     */
    options: PropTypes.oneOfType([
        PropTypes.arrayOf(
            PropTypes.oneOfType([
                PropTypes.string.isRequired,
                PropTypes.number.isRequired,
            ]).isRequired
        ),
        PropTypes.arrayOf(
            PropTypes.exact({
                label: PropTypes.oneOfType([
                    PropTypes.string.isRequired,
                    PropTypes.number.isRequired,
                ]).isRequired,
                value: PropTypes.oneOfType([
                    PropTypes.string.isRequired,
                    PropTypes.number.isRequired,
                ]).isRequired,
            }).isRequired
        ),
    ]),
    /**
     * isMulti Selection bool.
     */
    isMulti: PropTypes.bool,
    /**
     * close menu when selecting. if false keep menu open. default false
     */
    closeMenuOnSelect: PropTypes.bool,
    /**
     * hide the selection made or keep in list if false. default true
     */
    hideSelectedOptions: PropTypes.bool,
    /**
     * enable selection of all components in list, default true
     */
    allowSelectAll: PropTypes.bool,
    /**
     * clear selection default true
     */
    isClearable: PropTypes.bool,
    /**
     * disable dropdown default false
     */
    isDisabled: PropTypes.bool,
    /**
     * append style to the div of dropdown component
     */
    style: PropTypes.object,
    /**
     * Append a class to the div of dropdown component
     */
    className: PropTypes.string,
    /**
     * Label above the dropdown.
     */
    label: PropTypes.string,
    /**
     * Dash-assigned callback that gets fired when the input changes
     */
    setProps: PropTypes.func,
};

const defaultProps: Optionals<InferProps<typeof propTypes>> = {
    options: [],
    value: [],
    isMulti: true,
    closeMenuOnSelect: false,
    hideSelectedOptions: true,
    allowSelectAll: true,
    isClearable: true,
    isDisabled: false,
    style: {},
    className: "",
    label: "",
    setProps: (): void => {
        return;
    },
};

/**
 * React Select expect type {label: data, value: data} for both options and values
 * The user have the possibility to pass options as only arrays of strings or numbers
 * We fix the logic here to handle the items and transform to the expected type.
 * We also return the value in the callback to match the type of options we received.
 * If it is not a Multi we return the value selected as a number or string
 */

type DropDownItem = {
    label: string | number;
    value: string | number;
};

type ValueDropDownItem<T> = T extends true ? DropDownItem : DropDownItem[];

type ItemInputTypes =
    | DropDownItem[]
    | DropDownItem
    | (string | number)[]
    | string
    | number;

const convertToDropDownItems = (items: ItemInputTypes): DropDownItem[] => {
    if (typeof items === "string" || typeof items === "number") {
        return [{ label: items, value: items }];
    } else if (Array.isArray(items)) {
        return items.map((option) =>
            typeof option === "string" || typeof option === "number"
                ? { label: option, value: option }
                : option
        );
    } else if (typeof items === "object") {
        return [items];
    } else {
        return items;
    }
};

const getType = (
    items: ItemInputTypes
): "primitive" | "array" | "objectArray" | "object" => {
    if (typeof items === "string" || typeof items === "number") {
        return "primitive";
    } else if (Array.isArray(items)) {
        if (items.length > 0) {
            const firstOption = items[0];
            if (
                typeof firstOption === "string" ||
                typeof firstOption === "number"
            ) {
                return "array";
            } else {
                return "objectArray";
            }
        } else {
            return "array";
        }
    } else {
        return "object";
    }
};

/**
 * Multi selection dropdown selector
 * Extension of the react selector
 */
const Option = (props: OptionProps) => {
    return (
        <div>
            <components.Option {...props}>
                <input
                    type="checkbox"
                    checked={props.isSelected}
                    onChange={() => null}
                />{" "}
                <label>{props.label}</label>
            </components.Option>
        </div>
    );
};

const allOption: DropDownItem = {
    label: "Select all",
    value: "*",
};

const ValueContainer = ({ children, ...props }: ValueContainerProps) => {
    const toBeRendered = children;

    return (
        <components.ValueContainer {...props}>
            {toBeRendered}
        </components.ValueContainer>
    );
};
interface MultiValuePropsEx extends MultiValueProps {
    data: { label: string; value: string } | unknown;
}

const MultiValue = (props: MultiValuePropsEx) => {
    const isLabelValueObject = (
        data: unknown
    ): data is { label: string; value: string } => {
        return (
            typeof data === "object" &&
            data !== null &&
            "label" in data &&
            "value" in data
        );
    };
    const labelToBeDisplayed = isLabelValueObject(props.data)
        ? `${props.data.label}`
        : "";

    return (
        <components.MultiValue {...props}>
            <span>{labelToBeDisplayed}</span>
        </components.MultiValue>
    );
};

export const Dropdown: React.FC<InferProps<typeof propTypes>> = (
    props: InferProps<typeof propTypes>
): JSX.Element => {
    const {
        id,
        style,
        className,
        label,
        value,
        options,
        isMulti,
        closeMenuOnSelect,
        hideSelectedOptions,
        allowSelectAll,
        isClearable,
        isDisabled,
        setProps,
    } = getPropsWithMissingValuesSetToDefault(props, defaultProps);

    const options_input = convertToDropDownItems(options);

    const selection_value = (
        options: ItemInputTypes,
        selections: DropDownItem[],
        isMulti: boolean
    ): ItemInputTypes => {
        switch (getType(options)) {
            case "array":
                return isMulti
                    ? selections.map((selection) => selection.value)
                    : selections.map((selection) => selection.value)[0];
            default:
                return isMulti
                    ? selections
                    : selections.map((selection) => selection.value)[0];
        }
    };
    const handleChange = (selected: ValueDropDownItem<typeof isMulti>) => {
        let set_selected: DropDownItem[] = [];
        if (
            typeof selected === "object" &&
            selected !== null &&
            Array.isArray(selected) &&
            selected.length > 0
        ) {
            set_selected = selected;
            if (selected[selected.length - 1].value === allOption.value) {
                set_selected = options_input.filter(
                    (item) => item.label !== "Select all"
                );
            }
        } else if (typeof selected === "object" && !Array.isArray(selected)) {
            set_selected = [selected];
        }

        setProps({
            value:
                selected === null || selected === undefined
                    ? []
                    : selection_value(options, set_selected, isMulti),
        });
    };

    return (
        <div id={id} style={style} className={className}>
            {label && <label>{label}</label>}
            <ReactSelect
                options={
                    (typeof value === "object" &&
                        value !== null &&
                        Array.isArray(value) &&
                        options_input.length === value.length) ||
                    !allowSelectAll ||
                    !isMulti
                        ? options_input
                        : [allOption, ...options_input]
                }
                isMulti={isMulti}
                closeMenuOnSelect={closeMenuOnSelect}
                hideSelectedOptions={hideSelectedOptions}
                components={
                    isMulti
                        ? {
                              Option,
                              MultiValue,
                              ValueContainer,
                          }
                        : undefined
                }
                onChange={(selected) =>
                    handleChange(selected as ValueDropDownItem<typeof isMulti>)
                }
                value={convertToDropDownItems(value)}
                isClearable={isClearable}
                isDisabled={isDisabled}
            />
        </div>
    );
};

Dropdown.defaultProps = defaultProps;
Dropdown.propTypes = propTypes;
