import { MessageSquare, Github } from 'lucide-react';
import { Separator } from '@/components/ui/separator';

export function Footer() {
  return (
    <footer className="border-t py-6 md:py-0">
      <div className="w-full max-w-[1400px] mx-auto flex h-14 items-center justify-between px-4 md:px-6">
        <div className="flex items-center gap-2">
          <MessageSquare className="h-5 w-5" />
          <p className="text-sm text-muted-foreground">
            Context Chat © {new Date().getFullYear()}. All rights reserved.
          </p>
        </div>
        <div className="flex items-center">
          <a 
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="text-muted-foreground hover:text-foreground"
          >
            <Github className="h-5 w-5" />
            <span className="sr-only">GitHub</span>
          </a>
        </div>
      </div>
    </footer>
  );
}