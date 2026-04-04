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

  register: (name: string, rules?: ValidationRule) => void;
  unregister: (name: string) => void;

  getFieldProps: (name: string) => {
    name: string;
    value: any;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onBlur: () => void;
  };

  setValue: (name: string, value: any) => void;

  validateField: (name: string, valueOverride?: any) => string | null;
  validateAll: () => boolean;

  handleSubmit: (
    onSubmit: (values: FormValues) => void,
  ) => (e: React.SubmitEvent) => void;
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
     Register (SIDE EFFECT ONLY)
  ========================= */
  const register = (name: string, rules?: ValidationRule) => {
    setFields((prev) => {
      if (prev[name]) return prev;

      return {
        ...prev,
        [name]: { name, rules },
      };
    });
  };

  const unregister = (name: string) => {
    setFields((prev) => {
      const updated = { ...prev };
      delete updated[name];
      return updated;
    });

    setValues((prev) => {
      const updated = { ...prev };
      delete updated[name];
      return updated;
    });

    setErrors((prev) => {
      const updated = { ...prev };
      delete updated[name];
      return updated;
    });

    setTouched((prev) => {
      const updated = { ...prev };
      delete updated[name];
      return updated;
    });
  };

  /* =========================
     Field Props (PURE)
  ========================= */
  const getFieldProps = (name: string) => {
    return {
      name,

      // ✅ Controlled for normal inputs
      value: values[name] ?? "",

      onChange: (e: React.ChangeEvent<HTMLInputElement>) => {
        const target = e.target;

        let value: any;

        if (target.type === "file") {
          value = target.files; // ✅ FileList
        } else {
          value = target.value;
        }

        setValues((prev) => ({
          ...prev,
          [name]: value,
        }));

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
     Validation
  ========================= */
  const validateField = (name: string, valueOverride?: any): string | null => {
    const field = fields[name];
    if (!field) return null;

    const value = valueOverride !== undefined ? valueOverride : values[name];
    const rules = field.rules;

    let error: string | null = null;

    if (rules) {
      if (rules.required && !value) {
        error = rules.required;
      }

      if (!error && rules.minLength && value?.length < rules.minLength.value) {
        error = rules.minLength.message;
      }

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

  const validateAll = () => {
    let isValid = true;

    Object.keys(fields).forEach((name) => {
      const error = validateField(name);
      if (error) isValid = false;
    });

    return isValid;
  };

  /* =========================
     Submit
  ========================= */
  const handleSubmit =
    (onSubmit: (values: FormValues) => void) => (e: React.SubmitEvent) => {
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
    unregister,
    getFieldProps,
    setValue,
    validateField,
    validateAll,
    handleSubmit,
  };
};
