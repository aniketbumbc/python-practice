export default function Spinner({ size = 16 }: { size?: number }) {
  return (
    <span
      className="inline-block animate-spin rounded-full border-2 border-border-strong border-t-primary"
      style={{ width: size, height: size }}
      aria-label="Loading"
    />
  );
}