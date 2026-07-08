"use client";
import { useEffect, useState } from "react";
import type { Post, ListStatus } from "@/lib/types";
import FeedGrid from "@/components/feed/FeedGrid";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import { fetchPosts } from "@/lib/mock";

const TOPICS = ["All", "Engineering", "Design", "Product", "AI"];

export default function HomePage() {
  const [status, setStatus] = useState<ListStatus>("loading");
  const [items, setItems] = useState<Post[]>([]);
  const [topic, setTopic] = useState("All");

  const load = () => {
    setStatus("loading");
    // Using mock data until the FastAPI backend endpoint is wired up.
    // Real fetch, kept for when the backend is ready:
    // fetch("/api/posts")
    //   .then((r) => r.json())
    //   .then((data: Post[]) => { setItems(data); setStatus(data.length ? "success" : "empty"); })
    //   .catch(() => setStatus("error"));
    fetchPosts()
      .then((data: Post[]) => { setItems(data); setStatus(data.length ? "success" : "empty"); })
      .catch(() => setStatus("error"));
  };
  useEffect(load, []);

  const visibleItems = topic === "All" ? items : items.filter((p) => p.topic === topic);

  return (
    <>
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <h1 className="font-serif text-[32px] font-bold text-ink">Latest posts</h1>
          <p className="text-muted mt-1">Fresh writing from the community.</p>
        </div>
        <div className="flex flex-wrap gap-2 justify-end">
          {TOPICS.map((t) => (
            <button
              key={t}
              onClick={() => setTopic(t)}
              className={cn("focus-ring cursor-pointer px-3 py-1.5 rounded-full text-sm border transition-colors",
                topic === t ? "bg-primary text-ink border-primary" : "bg-surface text-text border-border-strong hover:border-muted")}
            >{t}</button>
          ))}
        </div>
      </div>

      <FeedGrid status={status} items={visibleItems} onRetry={load} />

      {status === "success" && (
        <div className="mt-8 flex justify-center">
          <Button variant="secondary">Load more</Button>
        </div>
      )}
    </>
  );
}