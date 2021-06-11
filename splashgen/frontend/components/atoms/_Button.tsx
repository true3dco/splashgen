import Link from "next/Link";

// TODO: Dedupe with NavContentLayout
export interface LinkConfig {
  href: string;
  text: string;
}

export interface _ButtonProps {
  classNames?: string[];
  link?: LinkConfig;
  text?: string;
}

export default function _Button({
  classNames = [],
  text = "",
  link,
}: _ButtonProps) {
  if (link) {
    return (
      <Link href={link.href}>
        <a className={classNames.join(" ")}>{link.text}</a>
      </Link>
    );
  }

  return <button className={classNames.join(" ")}>{text}</button>;
}
