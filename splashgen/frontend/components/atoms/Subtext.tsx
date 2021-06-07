export interface SubtextProps {
  text: string;
}

export default function Subtext({ text }: SubtextProps) {
  return <p className="lead text-muted">{text}</p>;
}
