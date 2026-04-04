import { Form } from "@/shared/components/Form/Form";
import { FormField } from "@/shared/components/Form/FormField";
import { Input } from "@/shared/components/Input";
import { useToastContext } from "@/shared/components/Toast/ToastContext";
import { useUploadDocument } from "../hooks/useUploadDocument";

export default function DocumentsPage() {
  const { uploadDocument, isLoading } = useUploadDocument();
  const { showPromise } = useToastContext();

  const handleSubmit = async (values: Record<string, any>) => {
    const file: File | undefined = values.file?.[0];

    if (!file) return;

    const result = await showPromise(
      () => uploadDocument(file),
      {
        loading: "Uploading document...",
        success: "Document uploaded successfully",
        error: "Upload failed",
      }
    );

    if (result.success) {
      // later: refresh list
      console.log("Uploaded:", result.data);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <section>
        <h1 className="text-2xl font-semibold text-white">Documents</h1>
        <p className="text-gray-400 text-sm mt-1">
          Upload documents to power your AI chat.
        </p>
      </section>

      {/* Upload Form */}
      <Form onSubmit={handleSubmit}>
        <div className="bg-gray-900 p-6 rounded-lg border border-gray-700">
          <div className="max-w-md space-y-4">
            <h2 className="text-lg font-medium text-white">
              Upload Document
            </h2>

            {/* File Input */}
            <FormField
              name="file"
              rules={{ required: "File is required" }}
            >
              <Input
                type="file"
                label="Choose File"
                className="w-full p-2 rounded bg-gray-800 text-white"
              />
            </FormField>

            {/* Submit */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 p-2 rounded disabled:opacity-50"
            >
              {isLoading ? "Uploading..." : "Upload"}
            </button>
          </div>
        </div>
      </Form>

      {/* Placeholder List */}
      <section className="bg-gray-900 border border-gray-700 rounded-lg p-6">
        <h2 className="text-lg font-medium text-white mb-4">
          Your Documents
        </h2>

        <p className="text-sm text-gray-400">
          No documents uploaded yet.
        </p>
      </section>
    </div>
  );
}