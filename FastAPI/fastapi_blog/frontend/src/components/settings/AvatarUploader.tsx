"use client";
import { useRef, useState } from "react";
import Avatar from "@/components/ui/Avatar";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";

type Props = {
  src?: string;
  onUpload: (file: File, onProgress: (pct: number) => void) => Promise<{ ok: true } | { ok: false; error: string }>;
  onRemove: () => Promise<{ ok: true } | { ok: false; error: string }>;
};

export default function AvatarUploader({ src, onUpload, onRemove }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [removing, setRemoving] = useState(false);
  const [progress, setProgress] = useState(0);
  const [fileName, setFileName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFile = async (file: File) => {
    if (!file.type.startsWith("image/")) {
      setError("Only JPG or PNG images are supported.");
      return;
    }
    setError(null);
    setFileName(file.name);
    setProgress(0);
    setUploading(true);
    const result = await onUpload(file, setProgress);
    setUploading(false);
    if (!result.ok) setError(result.error);
  };

  const remove = async () => {
    setError(null);
    setRemoving(true);
    const result = await onRemove();
    setRemoving(false);
    if (!result.ok) setError(result.error);
  };

  return (
    <div>
      <p className="text-[13px] font-medium text-text mb-1.5">Avatar</p>
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          const file = e.dataTransfer.files?.[0];
          if (file) handleFile(file);
        }}
        className={cn(
          "rounded-2xl border-2 border-dashed p-5 flex flex-col items-center text-center gap-3 transition-colors",
          dragOver ? "border-primary bg-tint" : "border-border-strong"
        )}
      >
        <Avatar src={src} size={96} />

        {uploading ? (
          <div className="w-full">
            <div className="h-1.5 w-full rounded-full bg-divider overflow-hidden">
              <div className="h-full bg-primary transition-[width]" style={{ width: `${progress}%` }} />
            </div>
            <p className="mt-1.5 text-xs text-subtle font-mono">Uploading… {progress}% · {fileName}</p>
          </div>
        ) : (
          <p className="text-sm text-muted">Drag an image here, or</p>
        )}

        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => inputRef.current?.click()} disabled={uploading || removing}>Choose file</Button>
          {src && (
            <Button variant="ghost" className="text-danger" onClick={remove} disabled={uploading || removing}>
              {removing ? "Removing…" : "Remove"}
            </Button>
          )}
        </div>
        <p className="text-xs text-subtle">JPG or PNG · max 5 MB · cropped to square</p>
        {error && <p className="text-xs text-danger">{error}</p>}

        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFile(file);
            e.target.value = "";
          }}
        />
      </div>
    </div>
  );
}
