import _Button, { _ButtonProps } from "./_Button";

export type SecondaryButtonProps = Omit<_ButtonProps, "classNames">;

export default function SecondaryButton({ link, text }: SecondaryButtonProps) {
  return (
    <_Button
      classNames={["btn", "btn-lg", "btn-outline-secondary"]}
      link={link!}
      text={text!}
    />
  );
}
