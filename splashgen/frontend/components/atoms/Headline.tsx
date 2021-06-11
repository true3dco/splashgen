export interface HeadlineProps {
  text: string;
}

export default function Headline({ text }: HeadlineProps) {
  return <h1 className="display-5 fw-bold">{text}</h1>;
}
