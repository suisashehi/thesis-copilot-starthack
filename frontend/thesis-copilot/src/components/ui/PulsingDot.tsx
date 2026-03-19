export function PulsingDot() {
  return (
    <span className="relative flex size-2">
      <span
        className="absolute inline-flex h-full w-full animate-ping rounded-full opacity-75"
        style={{ backgroundColor: '#22c55e' }}
      />
      <span
        className="relative inline-flex size-2 rounded-full"
        style={{ backgroundColor: '#22c55e' }}
      />
    </span>
  )
}