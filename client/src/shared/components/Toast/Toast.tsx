type ToastProps = {
  message: string;
  type?: "success" | "error" | "loading";
};

export default function Toast({ message, type = "success" }: ToastProps) {
  const base =
    "px-4 py-2 rounded shadow-lg text-white animate-slide-in";

  const variants = {
    success: "bg-green-600",
    error: "bg-red-600",
    loading: "bg-blue-600",
  };

  return (
    <div className={`${base} ${variants[type]}`}>
      {type === "loading" ? "⏳ " : null}
      {message}
    </div>
  );
}