import _Button, { _ButtonProps } from "./_Button";

export type PrimaryButtonProps = Omit<_ButtonProps, "classNames">;

export default function PrimaryButton({ link, text }: PrimaryButtonProps) {
  return (
    <_Button
      classNames={["btn", "btn-lg", "btn-primary"]}
      link={link!}
      text={text!}
    />
  );
}
