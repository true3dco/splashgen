import Accordion from "react-bootstrap/Accordion";
import CardGroup from "react-bootstrap/CardGroup";
import Card from "react-bootstrap/Card";
import { Check2 } from "react-bootstrap-icons";
import StackLayout from "../layouts/StackLayout";
import PrimaryButton from "../atoms/PrimaryButton";
import SecondaryButton from "../atoms/SecondaryButton";

export interface FeatureList {
  headline?: string;
  features: string[];
}

export interface Tier {
  name: string;
  pricePerMonth: number;
  callToAction: {
    href: string;
    text: string;
  };
  description?: string;
  featureList?: FeatureList;
  recommended?: boolean;
}

export interface Faq {
  question: string;
  answer: string;
}

export interface PricingStructure {
  tiers: Tier[];
  faqs?: Faq[];
}

export interface PricingUIProps {
  structure: PricingStructure;
}

export default function PricingUI({ structure }: PricingUIProps) {
  return (
    <StackLayout direction="vertical" spacing={16}>
      <CardGroup>
        {structure.tiers.map((tier) => (
          <Card key={tier.name}>
            <Card.Body>
              <Card.Title className={tier.recommended ? "text-primary" : ""}>
                {tier.name}
              </Card.Title>
              {tier.description && <Card.Text>{tier.description}</Card.Text>}
              <Card.Text>
                <span className="display-4 d-block">${tier.pricePerMonth}</span>
                <span className="d-block text-muted">per month</span>
              </Card.Text>
              {tier.recommended ? (
                <PrimaryButton link={tier.callToAction} />
              ) : (
                <SecondaryButton link={tier.callToAction} />
              )}
              {tier.featureList && (
                <Card.Text>
                  <p className="fw-bold">
                    {tier.featureList.headline || "Includes"}:
                  </p>
                  <ul className="list-unstyled">
                    {tier.featureList.features.map((feature) => (
                      <li key={feature}>
                        <Check2 /> {feature}
                      </li>
                    ))}
                  </ul>
                </Card.Text>
              )}
            </Card.Body>
          </Card>
        ))}
      </CardGroup>
      {structure.faqs && (
        <section>
          <h2>FAQs</h2>
          <Accordion flush>
            {structure.faqs.map((faq, i) => (
              <Accordion.Item key={i} eventKey={String(i)}>
                <Accordion.Header>
                  <span className="fw-bold">{faq.question}</span>
                </Accordion.Header>
                <Accordion.Body>{faq.answer}</Accordion.Body>
              </Accordion.Item>
            ))}
          </Accordion>
        </section>
      )}
    </StackLayout>
  );
}
