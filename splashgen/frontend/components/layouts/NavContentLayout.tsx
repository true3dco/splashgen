import { PropsWithChildren } from "react";
import { useRouter } from "next/router";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Link from "next/Link";
import { useBranding } from "../atoms/branding";

interface LinkConfig {
  href: string;
  text: string;
}

interface NavContentLayoutProps {
  links: LinkConfig[];
  actions: LinkConfig[];
}

export default function NavContentLayout({
  children,
  links,
  actions,
}: PropsWithChildren<NavContentLayoutProps>) {
  const { asPath } = useRouter();
  const branding = useBranding();
  return (
    <>
      <header>
        <Navbar bg={branding.theme} variant={branding.theme} expand="md">
          <Container fluid>
            <Link href="/" passHref>
              <Navbar.Brand className="d-flex align-items-center">
                {/* Used the aspect ratio of the SVG image, and we used an SVG image */}
                {branding.logo && (
                  <img
                    src={branding.logo}
                    className="me-2"
                    width={18}
                    height={30}
                    alt={`${branding.name} logo`}
                  />
                )}
                {branding.name}
              </Navbar.Brand>
            </Link>
            <Navbar.Toggle aria-controls="nav-content-layout__nav" />
            <Navbar.Collapse id="nav-content-layout__nav">
              <Nav className="me-auto">
                {links.map(({ href, text }) => (
                  <Link key={href} href={href} passHref>
                    <Nav.Link active={asPath === href}>{text}</Nav.Link>
                  </Link>
                ))}
              </Nav>
              <Nav>
                {actions.map(({ href, text }) => (
                  <Link key={href} href={href} passHref>
                    <Nav.Link active={asPath === href}>{text}</Nav.Link>
                  </Link>
                ))}
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      </header>

      <Container as="main" fluid className="py-5">
        {children}
      </Container>
    </>
  );
}
