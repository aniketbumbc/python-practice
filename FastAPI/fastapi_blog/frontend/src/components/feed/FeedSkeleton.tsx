export default function FeedSkeleton() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-[22px]">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="bg-surface border border-border rounded-[14px] overflow-hidden">
          <div className="h-[140px] bg-divider animate-pulse" />
          <div className="p-4 space-y-3">
            <div className="h-5 w-3/4 bg-divider rounded animate-pulse" />
            <div className="h-4 w-full bg-divider rounded animate-pulse" />
            <div className="flex items-center gap-2 pt-1">
              <div className="w-6 h-6 rounded-full bg-divider animate-pulse" />
              <div className="h-3 w-24 bg-divider rounded animate-pulse" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}