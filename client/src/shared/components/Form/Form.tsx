import React from "react";
import { useForm } from "./useForm";
import { FormContext } from "./formContext";

type FormProps = {
  children: React.ReactNode;
  onSubmit: (
    values: Record<string, any>,
    actions: { reset: () => void },
  ) => void;
  clearOnSubmit?: boolean;
};

export const Form = ({ children, onSubmit, clearOnSubmit }: FormProps) => {
  const form = useForm();

  return (
    <FormContext.Provider value={form}>
      <form
        onSubmit={form.handleSubmit((values, actions) => {
          onSubmit(values, actions);
          if (clearOnSubmit) {
            actions.reset();
          }
        })}
      >
        {children}
      </form>
    </FormContext.Provider>
  );
};
