import { Children, PropsWithChildren, Fragment } from "react";

// TODO: Figure out a better way to keep this in sync w/ python
export type StackLayoutProps = PropsWithChildren<{
  direction: "horizontal" | "vertical";
  spacing?: number;
  alignx?: "start" | "end" | "center";
  aligny?: "start" | "end" | "center";
  className?: string;
}>;

export default function StackLayout({
  direction,
  spacing = 8,
  alignx = "start",
  aligny = "start",
  children,
  className,
}: StackLayoutProps) {
  const marginKey = `margin${direction === "horizontal" ? "Right" : "Bottom"}`;
  const len = Children.count(children);
  return (
    <div
      className={className || ""}
      style={{
        display: "flex",
        flexDirection: direction === "horizontal" ? "row" : "column",
        [direction === "horizontal" ? "justifyContent" : "alignItems"]:
          alignx === "center" ? alignx : `flex-${alignx}`,
        [direction === "horizontal" ? "alignItems" : "justifyContent"]:
          aligny === "center" ? aligny : `flex-${aligny}`,
      }}
    >
      {Children.map(children, (child, i) => (
        <Fragment key={i}>
          {child}
          {i < len - 1 && (
            <div
              role="presentation"
              style={{
                [marginKey]: i == len - 1 ? 0 : spacing,
                width: 1,
                height: 1,
              }}
            ></div>
          )}
        </Fragment>
      ))}
    </div>
  );
}
