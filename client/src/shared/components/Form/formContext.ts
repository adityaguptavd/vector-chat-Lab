import { createContext, useContext } from "react";
import { useForm } from "./useForm";

type FormContextType = ReturnType<typeof useForm> | null;

export const FormContext = createContext<FormContextType>(null);

export const useFormContext = () => {
  const context = useContext(FormContext);

  if (!context) {
    throw new Error("useFormContext must be used inside <Form />");
  }

  return context;
};