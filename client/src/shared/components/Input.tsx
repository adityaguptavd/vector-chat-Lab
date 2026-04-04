import { FormFieldInjectedProps } from "./Form/FormField";

type InputProps = {
  label?: string;
} & Partial<FormFieldInjectedProps> &
  React.InputHTMLAttributes<HTMLInputElement>;

export const Input = ({ label, error, type, ...props }: InputProps) => {
  return (
    <div className="flex flex-col gap-1">
      {label && <label>{label}</label>}

      <input
        {...props}
        type={type}
        // remove value for file inputs
        {...(type === "file" ? { value: undefined } : {})}
      />

      {error && <span className="text-red-500">{error}</span>}
    </div>
  );
};