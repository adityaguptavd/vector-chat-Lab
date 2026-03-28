import { useState } from "react";

/* =========================
   Types
========================= */

export type ValidationRule =
  | {
      required?: string;
      minLength?: { value: number; message: string };
      validate?: (value: any) => string | null;
    }
  | undefined;

type FieldConfig = {
  name: string;
  rules?: ValidationRule;
};

type FormValues = Record<string, any>;
type FormErrors = Record<string, string | null>;
type FormTouched = Record<string, boolean>;

type UseFormReturn = {
  values: FormValues;
  errors: FormErrors;
  touched: FormTouched;

  register: (name: string, rules?: ValidationRule) => {
    name: string;
    value: any;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onBlur: () => void;
  };

  setValue: (name: string, value: any) => void;
  validateField: (name: string) => string | null;
  validateAll: () => boolean;

  handleSubmit: (onSubmit: (values: FormValues) => void) => (e: React.SubmitEvent) => void;
};

/* =========================
   Hook
========================= */

export const useForm = (): UseFormReturn => {
  const [values, setValues] = useState<FormValues>({});
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<FormTouched>({});
  const [fields, setFields] = useState<Record<string, FieldConfig>>({});

  /* =========================
     Register Field
  ========================= */
  const register = (name: string, rules?: ValidationRule) => {
    // store field config
    if (!fields[name]) {
      setFields((prev) => ({
        ...prev,
        [name]: { name, rules },
      }));
    }

    return {
      name,
      value: values[name] || "",
      onChange: (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;

        setValues((prev) => ({
          ...prev,
          [name]: value,
        }));

        // live validation (optional but useful)
        validateField(name, value);
      },
      onBlur: () => {
        setTouched((prev) => ({
          ...prev,
          [name]: true,
        }));

        validateField(name);
      },
    };
  };

  /* =========================
     Set Value
  ========================= */
  const setValue = (name: string, value: any) => {
    setValues((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  /* =========================
     Validation Logic
  ========================= */
  const validateField = (name: string, valueOverride?: any): string | null => {
    const field = fields[name];
    if (!field) return null;

    const value = valueOverride !== undefined ? valueOverride : values[name];
    const rules = field.rules;

    let error: string | null = null;

    if (rules) {
      // required
      if (rules.required && !value) {
        error = rules.required;
      }

      // minLength
      if (!error && rules.minLength && value?.length < rules.minLength.value) {
        error = rules.minLength.message;
      }

      // custom validate
      if (!error && rules.validate) {
        error = rules.validate(value);
      }
    }

    setErrors((prev) => ({
      ...prev,
      [name]: error,
    }));

    return error;
  };

  /* =========================
     Validate All
  ========================= */
  const validateAll = () => {
    let isValid = true;

    Object.keys(fields).forEach((name) => {
      const error = validateField(name);
      if (error) isValid = false;
    });

    return isValid;
  };

  /* =========================
     Handle Submit
  ========================= */
  const handleSubmit =
    (onSubmit: (values: FormValues) => void) =>
    (e: React.SubmitEvent) => {
      e.preventDefault();

      const isValid = validateAll();

      if (!isValid) return;

      onSubmit(values);
    };

  return {
    values,
    errors,
    touched,
    register,
    setValue,
    validateField,
    validateAll,
    handleSubmit,
  };
};