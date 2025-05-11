import { Link, useLocation } from 'react-router-dom';
import { MessageSquare, Home, List, MessageCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from './ThemeToggle';

export function Navbar() {
  const location = useLocation();
  
  const navItems = [
    {
      name: 'Home',
      path: '/',
      icon: <Home className="h-4 w-4 mr-2" />,
    },
    {
      name: 'Challenge 1',
      path: '/chat',
      icon: <MessageSquare className="h-4 w-4 mr-2" />,
    },
    {
      name: 'Challenge 2',
      path: '/question',
      icon: <List className="h-4 w-4 mr-2" />,
    },
    {
      name: 'Challenge 3',
      path: '/simple-chat',
      icon: <MessageCircle className="h-4 w-4 mr-2" />,
    },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="w-full max-w-[1400px] mx-auto flex h-14 items-center px-4 md:px-6">
        <div className="mr-4 hidden md:flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <MessageSquare className="h-6 w-6" />
            <span className="hidden font-bold sm:inline-block">
              IsDBI Hack
            </span>
          </Link>
          <nav className="flex items-center space-x-2 text-sm font-medium">
            {navItems.map((item) => (
              <Link key={item.path} to={item.path}>
                <Button
                  variant={location.pathname === item.path ? "secondary" : "ghost"}
                  className={cn(
                    "gap-1 text-xs sm:text-sm",
                    location.pathname === item.path && "bg-muted"
                  )}
                >
                  {item.icon}
                  <span>{item.name}</span>
                </Button>
              </Link>
            ))}
          </nav>
        </div>
        
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center md:hidden">
            {navItems.map((item) => (
              <Link key={item.path} to={item.path}>
                <Button
                  variant={location.pathname === item.path ? "secondary" : "ghost"}
                  size="icon"
                  className={cn(
                    location.pathname === item.path && "bg-muted"
                  )}
                >
                  {item.icon}
                </Button>
              </Link>
            ))}
          </nav>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}