import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  ActivityIndicator,
  Platform,
  TouchableOpacity,
} from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useQuery } from '@tanstack/react-query';
import { fetchLegacy } from '@/lib/api';

const ACCENT = '#c9923a';
const ACCENT_LIGHT = '#ddb06a';
const BG = '#0e0a06';
const CARD_BG = '#1a1208';
const SURFACE = '#130d07';
const TEXT_PRIMARY = '#f0e6d0';
const TEXT_BODY = '#c8ad8a';
const TEXT_SECONDARY = '#b8956a';
const TEXT_MUTED = '#7a5e3a';
const BORDER = '#2c1e0a';

function formatDate(str: string | null): string {
  if (!str) return '';
  const d = new Date(str);
  return d.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
}

export default function LegacyDetailScreen() {
  const { slug } = useLocalSearchParams<{ slug: string }>();
  const insets = useSafeAreaInsets();
  const router = useRouter();

  const { data: legacy, isLoading, error } = useQuery({
    queryKey: ['legacy', slug],
    queryFn: () => fetchLegacy(slug!),
    enabled: !!slug,
  });

  const botPad = Platform.OS === 'web' ? 34 : insets.bottom;

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={ACCENT} size="large" />
        <Text style={styles.loadingText}>Loading their story…</Text>
      </View>
    );
  }

  if (error || !legacy) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorTitle}>Story Not Found</Text>
        <Text style={styles.errorText}>This legacy may not exist or is pending review.</Text>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
          <Text style={styles.backBtnText}>Return to the Wall</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const initial = legacy.full_name?.charAt(0)?.toUpperCase() || '?';
  const paragraphs = legacy.story.split('\n').filter((p: string) => p.trim());

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={{ paddingBottom: botPad + 32 }}
      showsVerticalScrollIndicator={false}
    >
      <View style={styles.heroSection}>
        <View style={styles.portraitWrap}>
          {legacy.photo_url ? (
            <Image source={{ uri: legacy.photo_url }} style={styles.portrait} />
          ) : (
            <View style={styles.portraitPlaceholder}>
              <Text style={styles.portraitInitial}>{initial}</Text>
            </View>
          )}
        </View>

        <View style={styles.heroMeta}>
          {legacy.zone_name ? (
            <Text style={styles.zoneTag}>{legacy.zone_name.toUpperCase()}</Text>
          ) : null}
          <Text style={styles.heroName}>{legacy.full_name}</Text>
          {legacy.approved_at ? (
            <Text style={styles.heroDate}>Honored · {formatDate(legacy.approved_at)}</Text>
          ) : null}
        </View>
      </View>

      <View style={styles.storySection}>
        <View style={styles.storyDivider}>
          <View style={styles.dividerLine} />
          <Text style={styles.dividerLabel}>Their Story</Text>
          <View style={styles.dividerLine} />
        </View>

        {paragraphs.map((para: string, i: number) => (
          <Text key={i} style={styles.paragraph}>{para}</Text>
        ))}

        <View style={[styles.storyDivider, { marginTop: 32 }]}>
          <View style={styles.dividerLine} />
          <Text style={{ color: ACCENT, fontSize: 10, opacity: 0.5 }}>✦</Text>
          <View style={styles.dividerLine} />
        </View>
      </View>

      <View style={styles.sideCard}>
        <Text style={styles.sideCardTitle}>In Remembrance</Text>
        <View style={styles.sideCardDivider} />
        <View style={styles.sideRow}>
          <Text style={styles.sideDt}>Name</Text>
          <Text style={styles.sideDd}>{legacy.full_name}</Text>
        </View>
        {legacy.zone_name ? (
          <View style={styles.sideRow}>
            <Text style={styles.sideDt}>Region</Text>
            <Text style={styles.sideDd}>{legacy.zone_name}, Oromiyaa</Text>
          </View>
        ) : null}
        {legacy.approved_at ? (
          <View style={styles.sideRow}>
            <Text style={styles.sideDt}>Honored</Text>
            <Text style={styles.sideDd}>{formatDate(legacy.approved_at)}</Text>
          </View>
        ) : null}
      </View>

      <TouchableOpacity style={styles.returnBtn} onPress={() => router.back()}>
        <Text style={styles.returnBtnText}>← Return to the Wall</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: BG },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 40, gap: 12, backgroundColor: BG },
  loadingText: { color: TEXT_MUTED, fontSize: 14, fontStyle: 'italic' },
  errorTitle: { fontSize: 20, color: TEXT_SECONDARY, fontStyle: 'italic' },
  errorText: { fontSize: 14, color: TEXT_MUTED, textAlign: 'center' },
  backBtn: {
    marginTop: 8,
    borderWidth: 1,
    borderColor: 'rgba(201,146,58,0.3)',
    borderRadius: 3,
    paddingVertical: 10,
    paddingHorizontal: 20,
  },
  backBtnText: { color: ACCENT, fontSize: 14, letterSpacing: 0.4 },
  heroSection: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 16,
    padding: 20,
    paddingBottom: 24,
    backgroundColor: SURFACE,
    borderBottomWidth: 1,
    borderBottomColor: BORDER,
  },
  portraitWrap: {
    width: 90,
    height: 110,
    borderRadius: 2,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(201,146,58,0.25)',
  },
  portrait: { width: '100%', height: '100%' },
  portraitPlaceholder: {
    width: '100%',
    height: '100%',
    backgroundColor: '#120d05',
    alignItems: 'center',
    justifyContent: 'center',
  },
  portraitInitial: { fontSize: 36, color: ACCENT, opacity: 0.5, fontWeight: '200' },
  heroMeta: { flex: 1, paddingTop: 4 },
  zoneTag: {
    fontSize: 9,
    color: ACCENT,
    letterSpacing: 1,
    marginBottom: 6,
    opacity: 0.8,
  },
  heroName: {
    fontSize: 22,
    fontWeight: '300',
    color: TEXT_PRIMARY,
    letterSpacing: 0.3,
    lineHeight: 28,
    marginBottom: 8,
  },
  heroDate: { fontSize: 11, color: TEXT_MUTED, fontStyle: 'italic', letterSpacing: 0.2 },
  storySection: { padding: 20 },
  storyDivider: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 24,
  },
  dividerLine: { flex: 1, height: 1, backgroundColor: ACCENT, opacity: 0.2 },
  dividerLabel: {
    fontSize: 9,
    color: ACCENT,
    letterSpacing: 0.25,
    textTransform: 'uppercase',
    opacity: 0.6,
  },
  paragraph: {
    fontSize: 16,
    color: TEXT_BODY,
    lineHeight: 26,
    marginBottom: 16,
  },
  sideCard: {
    marginHorizontal: 20,
    marginBottom: 16,
    backgroundColor: CARD_BG,
    borderWidth: 1,
    borderColor: BORDER,
    borderTopWidth: 2,
    borderTopColor: 'rgba(201,146,58,0.25)',
    padding: 14,
    borderRadius: 2,
  },
  sideCardTitle: {
    fontSize: 9,
    color: TEXT_MUTED,
    textTransform: 'uppercase',
    letterSpacing: 0.12,
    fontWeight: '700',
  },
  sideCardDivider: { height: 1, backgroundColor: BORDER, marginVertical: 10 },
  sideRow: { flexDirection: 'row', gap: 12, marginBottom: 8, alignItems: 'flex-start' },
  sideDt: { width: 60, fontSize: 10, color: TEXT_MUTED, textTransform: 'uppercase', letterSpacing: 0.5, paddingTop: 2 },
  sideDd: { flex: 1, fontSize: 14, color: TEXT_SECONDARY },
  returnBtn: {
    marginHorizontal: 20,
    marginBottom: 8,
    paddingVertical: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: BORDER_LIGHT,
    borderRadius: 2,
  },
  returnBtnText: { color: TEXT_MUTED, fontSize: 13, letterSpacing: 0.4 },
});

const BORDER_LIGHT = '#3e2c12';
