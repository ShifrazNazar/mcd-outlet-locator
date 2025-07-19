import { useForm } from "react-hook-form";
import type { Outlet } from "./OutletMap";

interface ChatSearchBoxProps {
  setChatbotResults: (results: Outlet[] | null) => void;
  setChatbotError: (err: string | null) => void;
  chatbotLoading: boolean;
  setChatbotLoading: (loading: boolean) => void;
  chatbotError: string | null;
}

export default function ChatSearchBox({
  setChatbotResults,
  setChatbotError,
  chatbotLoading,
  setChatbotLoading,
}: ChatSearchBoxProps) {
  const { register, handleSubmit, reset, setValue, watch } = useForm<{
    query: string;
  }>({ defaultValues: { query: "" } });
  const watchedQuery = watch("query");

  const onSubmit = async ({ query }: { query: string }) => {
    query = query.trim();
    if (!query) {
      setChatbotResults(null);
      setChatbotError(null);
      return;
    }
    setChatbotLoading(true);
    setChatbotError(null);
    try {
      const res = await fetch("http://localhost:8000/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) throw new Error("Chatbot search failed");
      const data = await res.json();
      setChatbotResults(data.outlets);
      setChatbotLoading(false);
      if (!data.outlets.length)
        setChatbotError("No outlets found for your query.");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setChatbotError(err.message);
      } else {
        setChatbotError("Unknown error");
      }
      setChatbotLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="absolute top-5 left-1/2 -translate-x-1/2 z-[1000] bg-white/95 p-4 rounded-lg shadow flex gap-2 items-center min-w-[320px]"
      role="search"
      aria-label="Outlet search"
    >
      <label htmlFor="outlet-search" className="sr-only">
        Search outlets
      </label>
      <input
        id="outlet-search"
        type="search"
        {...register("query")}
        placeholder="Ask about outlets (e.g. 24 hours in KL, party, drive thru)"
        className="flex-1 min-w-[450px] p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
        autoFocus
        autoComplete="off"
        disabled={chatbotLoading}
        aria-label="Ask about outlets"
        onKeyDown={(e) => {
          if (e.key === "Escape") {
            setValue("query", "");
            setChatbotResults(null);
            setChatbotError(null);
          }
        }}
      />
      <button
        type="submit"
        className="px-4 py-2 rounded bg-blue-600 text-white font-semibold hover:bg-blue-700 disabled:opacity-60 flex items-center gap-2"
        disabled={chatbotLoading}
        aria-busy={chatbotLoading}
      >
        {chatbotLoading ? (
          <>
            <svg className="animate-spin h-4 w-4 mr-1" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8z"
              />
            </svg>
            Searching...
          </>
        ) : (
          "Search"
        )}
      </button>
      {watchedQuery && (
        <button
          type="button"
          onClick={() => {
            reset();
            setChatbotResults(null);
            setChatbotError(null);
          }}
          className="ml-1 bg-gray-200 rounded px-3 py-2 hover:bg-gray-300"
          disabled={chatbotLoading}
          aria-label="Clear search"
        >
          Clear
        </button>
      )}
    </form>
  );
}
