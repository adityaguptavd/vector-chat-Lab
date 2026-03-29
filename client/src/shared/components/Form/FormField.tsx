import React, { useEffect } from "react";
import { useFormContext } from "./formContext";
import type { ValidationRule } from "./useForm";

type FormFieldProps = {
  name: string;
  rules?: ValidationRule;
  children: React.ReactElement<FormFieldInjectedProps>;
};

export type FormFieldInjectedProps = {
  name: string;
  value: any;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur: () => void;
  error?: string | null;
};

export const FormField = ({ name, rules, children }: FormFieldProps) => {
  const {
    register,
    unregister,
    getFieldProps,
    errors,
    touched,
  } = useFormContext();

  // register safely (side effect)
  useEffect(() => {
    register(name, rules);

    return () => {
      unregister(name);
    };
  }, [name]);

  // pure read
  const field = getFieldProps(name);

  return React.cloneElement(children, {
    ...field,
    error: touched[name] ? errors[name] : null,
  });
};