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
    ]),
    options: PropTypes.arrayOf(
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
    isMulti: PropTypes.bool,
    closeMenuOnSelect: PropTypes.bool,
    hideSelectedOptions: PropTypes.bool,
    allowSelectAll: PropTypes.bool,
    isClearable: PropTypes.bool,
    isDisabled: PropTypes.bool,
    style: PropTypes.object,
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
    setProps: (): void => {
        return;
    },
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

const allOption = {
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

    const options_input: { label: string; value: string }[] = options.map(
        (option) => {
            if (
                typeof option === "object" &&
                option !== null &&
                !Array.isArray(option)
            ) {
                return {
                    label: String(option.label),
                    value: String(option.value),
                };
            } else {
                return {
                    label: String(option),
                    value: String(option),
                };
            }
        }
    );

    const handleChange = (
        selected: [{ label: string; value: string }] | unknown
    ) => {
        if (
            typeof selected === "object" &&
            selected !== null &&
            Array.isArray(selected) &&
            selected.length > 0
        ) {
            if (selected[selected.length - 1].value === allOption.value) {
                selected = options_input.filter(
                    (item) => item.label !== "Select all"
                );
            }
        }

        setProps({
            value: selected === null ? [] : selected,
        });
    };

    return (
        <div id={id} style={style}>
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
                components={{
                    Option,
                    MultiValue,
                    ValueContainer,
                }}
                onChange={handleChange}
                value={value}
                isClearable={isClearable}
                isDisabled={isDisabled}
            />
        </div>
    );
};

Dropdown.defaultProps = defaultProps;
Dropdown.propTypes = propTypes;
