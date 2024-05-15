type IconProps = {
  [k in 'href' | 'className']?: string
}

function MyIcon({ href, ...style }: IconProps) {
  return (
    <svg {...style}>
      <use href={href} />
    </svg>
  );
}

export default MyIcon;
