type IconProps = {
    href: string,
    [key:string]: any
}

function MyIcon({ href, ...style }: IconProps) {
  return (
    <svg {...style}>
      <use href={href} />
    </svg>
  );
}

export default MyIcon;
