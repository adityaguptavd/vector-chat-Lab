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
  const { register, errors, touched } = useFormContext();

  const field = register(name, rules);

  return React.cloneElement(children, {
    ...field,
    error: touched[name] ? errors[name] : null,
  });
};