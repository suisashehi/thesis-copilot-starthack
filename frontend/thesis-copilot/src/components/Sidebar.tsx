import { Home, BookOpen, Briefcase, Users } from 'lucide-react'
import { PulsingDot } from './ui/PulsingDot'

interface Props {
  profileSynced: boolean
}

const navItems = [
  { icon: Home, label: 'Home', active: true },
  { icon: BookOpen, label: 'Themen' },
  { icon: Briefcase, label: 'Jobs' },
  { icon: Users, label: 'Personen' },
]

export function Sidebar({ profileSynced }: Props) {
  return (
    <aside
      className="flex h-screen flex-col border-r"
      style={{
        width: 250,
        minWidth: 250,
        borderColor: 'var(--border)',
        backgroundColor: 'var(--sidebar)',
      }}
    >
      {/* Logo */}
      <div className="px-5 py-5">
        <span className="ds-title-sm font-semibold" style={{ color: 'var(--foreground)' }}>
          studyond ✦
        </span>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 pt-2">
        <p className="ds-caption px-2 pb-2" style={{ color: 'var(--muted-foreground)' }}>
          Persönlich
        </p>
        <ul className="space-y-0.5">
          {navItems.map(({ icon: Icon, label, active }) => (
            <li key={label}>
              <button
                className="flex w-full items-center gap-3 rounded-lg px-3 py-2 transition-colors duration-150"
                style={{
                  backgroundColor: active ? 'var(--accent)' : 'transparent',
                  color: active ? 'var(--foreground)' : 'var(--muted-foreground)',
                }}
              >
                <Icon size={16} />
                <span className="ds-small">{label}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* AI Status Meter */}
      <div
        className="mx-3 mb-5 rounded-xl p-4"
        style={{
          backgroundColor: 'var(--secondary)',
          border: '1px solid var(--border)',
        }}
      >
        <div className="mb-2 flex items-center gap-2">
          <PulsingDot />
          <span className="ds-badge" style={{ color: 'var(--foreground)' }}>
            Context: Active
          </span>
        </div>
        <div className="mb-1 flex items-center justify-between">
          <span className="ds-caption" style={{ color: 'var(--muted-foreground)' }}>
            Profile Sync
          </span>
          <span className="ds-caption" style={{ color: 'var(--muted-foreground)' }}>
            {profileSynced ? '100%' : '0%'}
          </span>
        </div>
        <div
          className="h-1.5 w-full overflow-hidden rounded-full"
          style={{ backgroundColor: 'var(--border)' }}
        >
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{
              width: profileSynced ? '100%' : '0%',
              background: 'linear-gradient(135deg, #7c3aed 0%, #2563eb 60%, #7c3aed 100%)',
            }}
          />
        </div>
      </div>
    </aside>
  )
}