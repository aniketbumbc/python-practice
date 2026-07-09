"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { useAuth } from "@/store/auth";
import { useToast } from "@/store/toast";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { signIn } = useAuth();
  const push = useToast((s) => s.push);
  const router = useRouter();

  const submit = async () => {
    setError(null);
    if (!username || !password) return setError("Incorrect username or password.");
    setLoading(true);
    const result = await signIn(username, password);
    setLoading(false);
    if (!result.ok) return setError(result.error);
    push("Welcome back");
    router.push("/");
  };

  return (
    <div className="max-w-[420px] mx-auto py-8">
      <Card className="p-7">
        <h1 className="font-serif text-2xl font-bold text-ink">Log in</h1>
        {error && <div className="mt-4 px-3 py-2 rounded-[9px] bg-danger-bg border border-danger-border text-sm text-danger">{error}</div>}
        <div className="mt-5 space-y-4">
          <Input label="Username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} />
          <Input
            label="Password" type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)}
            labelRight={<Link href="/forgot-password" className="text-xs text-accent">Forgot password?</Link>}
          />
          <Button className="w-full" onClick={submit} disabled={loading}>{loading ? "Logging in…" : "Log in"}</Button>
        </div>
        <p className="mt-4 text-sm text-muted text-center">No account? <Link href="/signup" className="text-accent">Sign up</Link></p>
      </Card>
    </div>
  );
}