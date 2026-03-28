type InputProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: string;
  label?: string;
  error?: string | null;
};

export default function Input({
  value,
  onChange,
  placeholder,
  type = "text",
  label,
  error,
}: InputProps) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="text-sm text-gray-300">{label}</label>
      )}

      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={`w-full p-2 rounded bg-gray-800 outline-none border ${
          error ? "border-red-500" : "border-gray-700"
        }`}
      />

      {error && (
        <p className="text-red-400 text-xs">{error}</p>
      )}
    </div>
  );
}