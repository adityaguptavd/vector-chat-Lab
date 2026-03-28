import { FormFieldInjectedProps } from "./Form/FormField";

type InputProps = {
  label?: string;
} & Partial<FormFieldInjectedProps> &
  React.InputHTMLAttributes<HTMLInputElement>;

export const Input = ({ label, error, ...props }: InputProps) => {
  return (
    <div className="flex flex-col gap-1">
      {label && <label>{label}</label>}

      <input {...props} />

      {error && <span className="text-red-500">{error}</span>}
    </div>
  );
};