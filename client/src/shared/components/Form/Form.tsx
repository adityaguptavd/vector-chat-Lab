import React from "react";
import { useForm } from "./useForm";
import { FormContext } from "./formContext";

type FormProps = {
  children: React.ReactNode;
  onSubmit: (values: Record<string, any>) => void;
};

export const Form = ({ children, onSubmit }: FormProps) => {
  const form = useForm();

  return (
    <FormContext.Provider value={form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {children}
      </form>
    </FormContext.Provider>
  );
};