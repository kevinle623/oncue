export function HeroVisual() {
  return (
    <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
      <svg
        className="absolute inset-0 size-full"
        viewBox="0 0 1200 800"
        preserveAspectRatio="xMidYMid slice"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden
      >
        <g opacity="0.18">
          {SPEED_LINES.map((line, i) => (
            <rect
              key={i}
              x="-600"
              y={line.y}
              width={line.w}
              height={line.h}
              fill="#1A1814"
              rx="0.5"
            >
              <animateTransform
                attributeName="transform"
                type="translate"
                from="-600 0"
                to="1800 0"
                dur={`${line.dur}s`}
                begin={`${line.begin}s`}
                repeatCount="indefinite"
              />
            </rect>
          ))}
        </g>

        <g transform="translate(600,400)">
          {SONAR_RINGS.map((ring, i) => (
            <circle
              key={i}
              r="80"
              fill="none"
              stroke="#1A1814"
              strokeWidth={ring.stroke}
              opacity="0"
            >
              <animate
                attributeName="r"
                values="80;260"
                dur="3s"
                repeatCount="indefinite"
                begin={`${ring.begin}s`}
              />
              <animate
                attributeName="opacity"
                values={`${ring.startOpacity};0`}
                dur="3s"
                repeatCount="indefinite"
                begin={`${ring.begin}s`}
              />
            </circle>
          ))}
          <circle
            r="60"
            fill="none"
            stroke="#1A1814"
            strokeWidth="0.5"
            opacity="0.12"
          />
          <circle
            r="40"
            fill="none"
            stroke="#1A1814"
            strokeWidth="0.5"
            opacity="0.18"
          />
          <circle r="3" fill="#1A1814" opacity="0.2">
            <animate
              attributeName="opacity"
              values="0.15;0.3;0.15"
              dur="3.5s"
              repeatCount="indefinite"
            />
          </circle>
        </g>

        <defs>
          <radialGradient id="heroGrad" cx="50%" cy="50%" r="60%">
            <stop offset="0%" stopColor="#F4F1EB" stopOpacity="0" />
            <stop offset="100%" stopColor="#F4F1EB" stopOpacity="0.85" />
          </radialGradient>
        </defs>
        <rect x="0" y="0" width="1200" height="800" fill="url(#heroGrad)" />
      </svg>
    </div>
  );
}

const SPEED_LINES = [
  { y: 220, w: 500, h: 1, dur: 3.2, begin: 0 },
  { y: 320, w: 340, h: 0.5, dur: 2.8, begin: 0.4 },
  { y: 400, w: 600, h: 1, dur: 3.5, begin: 0.9 },
  { y: 460, w: 280, h: 0.5, dur: 2.5, begin: 1.3 },
  { y: 540, w: 420, h: 0.5, dur: 3.8, begin: 0.2 },
  { y: 170, w: 380, h: 0.5, dur: 4.1, begin: 0.7 },
  { y: 620, w: 300, h: 0.5, dur: 2.9, begin: 1.1 },
];

const SONAR_RINGS = [
  { stroke: 1, begin: 0, startOpacity: 0.6 },
  { stroke: 0.8, begin: 1, startOpacity: 0.5 },
  { stroke: 0.6, begin: 2, startOpacity: 0.4 },
];
