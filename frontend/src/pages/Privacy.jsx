import { Helmet } from 'react-helmet-async';

export default function Privacy() {
  const lastUpdated = 'March 2026';

  return (
    <>
      <Helmet>
        <title>Privacy Policy — Oromo Legacy Wall</title>
        <meta
          name="description"
          content="Privacy policy for the Oromo Legacy Wall app and website."
        />
      </Helmet>

      <div style={{ maxWidth: '760px', margin: '0 auto', padding: '4rem 1.5rem 5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <div style={{ color: 'var(--accent)', fontSize: '1.5rem', marginBottom: '0.75rem' }}>✦</div>
          <h1 style={{ color: 'var(--text-primary)', fontSize: '2rem', marginBottom: '0.5rem' }}>
            Privacy Policy
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Last updated: {lastUpdated}
          </p>
        </div>

        <div style={{ color: 'var(--text-primary)', lineHeight: '1.9', fontSize: '1rem' }}>
          <Section title="Who We Are">
            <p>
              Oromo Legacy Wall is a digital memorial dedicated to honoring the lives of Oromo freedom
              fighters. The service is available at{' '}
              <a href="https://oromolegacywall.org" style={{ color: 'var(--accent)' }}>
                oromolegacywall.org
              </a>{' '}
              and through our iOS mobile application.
            </p>
          </Section>

          <Section title="What Information We Collect">
            <p>
              We collect only what is necessary to operate the memorial. Specifically:
            </p>
            <ul style={{ paddingLeft: '1.5rem', marginTop: '0.75rem' }}>
              <li style={{ marginBottom: '0.5rem' }}>
                <strong>Submission information</strong> — When you submit a hero record, you
                provide a name, story, photograph, region, occupation, and dates. This information
                becomes part of the public memorial record upon approval.
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                <strong>Tributes</strong> — When you leave a tribute message, the text is stored
                publicly alongside the hero's record.
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                <strong>Photos</strong> — Portrait photographs uploaded by submitters are stored
                securely on Cloudflare R2. They may be processed by AI restoration software
                (GFPGAN via Replicate) to improve quality.
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                <strong>Standard server logs</strong> — Our hosting infrastructure logs IP
                addresses and request metadata for security and stability purposes. These logs
                are not shared and are automatically deleted.
              </li>
            </ul>
          </Section>

          <Section title="What We Do Not Collect">
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li style={{ marginBottom: '0.5rem' }}>We do not require account registration.</li>
              <li style={{ marginBottom: '0.5rem' }}>We do not collect email addresses from visitors.</li>
              <li style={{ marginBottom: '0.5rem' }}>We do not use advertising networks or tracking pixels.</li>
              <li style={{ marginBottom: '0.5rem' }}>We do not sell or share personal data with third parties.</li>
            </ul>
          </Section>

          <Section title="How We Use Information">
            <p>
              Submitted hero information is reviewed by a moderator and, if approved, published to
              the public memorial wall. Photographs may be AI-enhanced for presentation quality.
              No submission data is used for advertising, profiling, or commercial purposes.
            </p>
          </Section>

          <Section title="Photo Library Access (Mobile App)">
            <p>
              The iOS app requests access to your photo library solely to allow you to select a
              portrait photograph when submitting a hero record. We do not access, copy, or store
              any photos other than the one you explicitly choose to upload.
            </p>
          </Section>

          <Section title="Third-Party Services">
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li style={{ marginBottom: '0.5rem' }}>
                <strong>Cloudflare R2</strong> — stores uploaded photographs.
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                <strong>Replicate (GFPGAN)</strong> — processes portrait photos for AI
                restoration. Photos are sent to Replicate's API and the enhanced result is
                saved; originals are retained.
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                <strong>Railway</strong> — hosts the backend API and database.
              </li>
            </ul>
          </Section>

          <Section title="Data Retention">
            <p>
              Approved hero records are intended to be permanent — they are a memorial. If you
              submitted a record and wish to have it removed or corrected, please contact us and
              we will review the request with care.
            </p>
          </Section>

          <Section title="Children's Privacy">
            <p>
              This service is not directed at children under 13. We do not knowingly collect
              information from children.
            </p>
          </Section>

          <Section title="Contact">
            <p>
              For any privacy-related questions or removal requests, please reach out through the
              website at{' '}
              <a href="https://oromolegacywall.org" style={{ color: 'var(--accent)' }}>
                oromolegacywall.org
              </a>
              .
            </p>
          </Section>
        </div>
      </div>
    </>
  );
}

function Section({ title, children }) {
  return (
    <div style={{ marginBottom: '2.5rem' }}>
      <h2
        style={{
          color: 'var(--accent)',
          fontSize: '1.1rem',
          fontWeight: 600,
          marginBottom: '0.75rem',
          borderBottom: '1px solid rgba(212,175,55,0.2)',
          paddingBottom: '0.4rem',
        }}
      >
        {title}
      </h2>
      {children}
    </div>
  );
}
