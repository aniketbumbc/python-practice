"use client";
import { useEffect, useState } from "react";
import FeedGrid from "@/components/feed/FeedGrid";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import { useBlogStore } from "@/store/blog";
import { useAuth } from "@/store/auth";

const TOPICS = ["Yours", "All", "Engineering", "Design", "Product", "AI"];

export default function HomePage() {
  const { posts, status, hasMore, fetchPosts, loadMore, searchQuery } = useBlogStore();
  const {currentUser} = useAuth()
  const [topic, setTopic] = useState(currentUser ? "Yours" : "All");

  const topics = currentUser ? TOPICS : TOPICS.filter((t) => t !== "Yours");
  const effectiveTopic = currentUser ? topic : topic === "Yours" ? "All" : topic;

  useEffect(() => {
    fetchPosts({ skip: 0, limit: 10 });
  }, [fetchPosts]);

  let visibleItems;
  if (effectiveTopic === "All") {
    visibleItems = posts;
  } else if (effectiveTopic === "Yours") {
    visibleItems = posts.filter((p) => currentUser?.id === p.author.id);
  } else {
    visibleItems = posts.filter((p) => p.topic === effectiveTopic);
  }

  const query = searchQuery.trim().toLowerCase();
  if (query) {
    visibleItems = visibleItems.filter((p) =>
      p.title.toLowerCase().includes(query) ||
      p.content.toLowerCase().includes(query) ||
      p.topic.toLowerCase().includes(query) ||
      p.author.username.toLowerCase().includes(query)
    );
  }

  return (
    <>
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <h1 className="font-serif text-[32px] font-bold text-ink">Latest posts</h1>
          <p className="text-muted mt-1">Fresh writing from the community.</p>
        </div>
        <div className="flex flex-wrap gap-2 justify-end">
          {topics.map((text) => (
            <button
              key={text}
              onClick={() => setTopic(text)}
              className={cn("focus-ring cursor-pointer px-3 py-1.5 rounded-full text-sm border transition-colors",
                effectiveTopic === text ? "bg-primary text-ink border-primary" : "bg-surface text-text border-border-strong hover:border-muted")}
            >{text}</button>
          ))}
        </div>
      </div>

      <FeedGrid
        status={status}
        items={visibleItems}
        onRetry={() => fetchPosts({ skip: 0, limit: 10 })}
        emptyTitle={query ? `No posts match “${searchQuery.trim()}”` : undefined}
        emptyCta={query ? <></> : undefined}
      />

      {status === "success" && hasMore && !query && (
        <div className="mt-8 flex justify-center">
          <Button variant="secondary" onClick={loadMore}>Load more</Button>
        </div>
      )}
    </>
  );
}