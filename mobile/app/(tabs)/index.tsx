import React, { useState, useCallback, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TextInput,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  RefreshControl,
  Platform,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import { fetchLegacies, fetchZones, LegacyItem, Zone } from '@/lib/api';
import { useLang } from '@/lib/lang';

const ACCENT = '#c9923a';
const ACCENT_LIGHT = '#ddb06a';
const BG = '#0e0a06';
const CARD_BG = '#1a1208';
const SURFACE = '#130d07';
const TEXT_PRIMARY = '#f0e6d0';
const TEXT_SECONDARY = '#b8956a';
const TEXT_MUTED = '#7a5e3a';
const BORDER = '#2c1e0a';

function formatDate(str: string | null): string {
  if (!str) return '';
  const d = new Date(str);
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
}

function LegacyCard({ item, onPress, rememberedLabel, readMoreLabel }: {
  item: LegacyItem;
  onPress: () => void;
  rememberedLabel: string;
  readMoreLabel: string;
}) {
  const initial = item.full_name?.charAt(0)?.toUpperCase() || '?';
  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.85}>
      <View style={styles.cardAccentBar} />
      <View style={styles.cardRow}>
        <View style={styles.cardPhotoWrap}>
          {item.photo_url ? (
            <Image source={{ uri: item.photo_url }} style={styles.cardPhoto} />
          ) : (
            <View style={styles.cardInitialWrap}>
              <Text style={styles.cardInitial}>{initial}</Text>
            </View>
          )}
        </View>
        <View style={styles.cardContent}>
          <Text style={styles.cardName} numberOfLines={1}>{item.full_name}</Text>
          {item.occupation ? (
            <Text style={styles.cardOccupation} numberOfLines={1}>{item.occupation}</Text>
          ) : null}
          {item.zone_name ? (
            <Text style={styles.cardZone}>{item.zone_name}</Text>
          ) : null}
          <Text style={styles.cardStory} numberOfLines={2}>{item.story_preview}</Text>
          {item.approved_at ? (
            <Text style={styles.cardDate}>{rememberedLabel} · {formatDate(item.approved_at)}</Text>
          ) : null}
        </View>
      </View>
      <View style={styles.cardFooter}>
        <Text style={styles.cardReadMore}>{readMoreLabel}</Text>
        <Ionicons name="chevron-forward" size={12} color={ACCENT} />
      </View>
    </TouchableOpacity>
  );
}

function ZoneFilter({
  zones,
  selected,
  onSelect,
  allZonesLabel,
}: {
  zones: Zone[];
  selected: string;
  onSelect: (slug: string) => void;
  allZonesLabel: string;
}) {
  return (
    <FlatList
      horizontal
      data={[{ id: 0, name: allZonesLabel, slug: '' }, ...zones]}
      keyExtractor={(z) => String(z.id)}
      contentContainerStyle={styles.zoneList}
      showsHorizontalScrollIndicator={false}
      renderItem={({ item }) => {
        const active = item.slug === selected;
        return (
          <TouchableOpacity
            style={[styles.zoneChip, active && styles.zoneChipActive]}
            onPress={() => onSelect(item.slug)}
            activeOpacity={0.7}
          >
            <Text style={[styles.zoneChipText, active && styles.zoneChipTextActive]}>
              {item.name}
            </Text>
          </TouchableOpacity>
        );
      }}
    />
  );
}

export default function WallScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang, setLang, t } = useLang();
  const [query, setQuery] = useState('');
  const [search, setSearch] = useState('');
  const [zone, setZone] = useState('');
  const [page, setPage] = useState(1);
  const inputRef = useRef<TextInput>(null);

  const { data: zonesData } = useQuery({
    queryKey: ['zones'],
    queryFn: fetchZones,
  });

  const { data, isLoading, isFetching, refetch } = useQuery({
    queryKey: ['legacies', search, zone, page],
    queryFn: () => fetchLegacies({ q: search, zone, page }),
    placeholderData: (prev) => prev,
  });

  const legacies = data?.results || [];
  const hasMore = !!data?.next;

  const handleSearch = useCallback(() => {
    setSearch(query.trim());
    setPage(1);
    inputRef.current?.blur();
  }, [query]);

  const handleZone = useCallback((slug: string) => {
    setZone(slug);
    setPage(1);
  }, []);

  const topPad = Platform.OS === 'web' ? 67 : insets.top;

  return (
    <View style={[styles.container, { paddingTop: topPad }]}>
      <View style={styles.header}>
        <View style={styles.headerRow}>
          <View style={styles.headerText}>
            <Text style={styles.headerTitle}>{t('wall_title')}</Text>
            <Text style={styles.headerSub}>{t('wall_sub')}</Text>
          </View>
          <View style={styles.langToggle}>
            <TouchableOpacity
              style={[styles.langBtn, lang === 'en' && styles.langBtnActive]}
              onPress={() => setLang('en')}
            >
              <Text style={[styles.langBtnText, lang === 'en' && styles.langBtnTextActive]}>EN</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.langBtn, lang === 'om' && styles.langBtnActive]}
              onPress={() => setLang('om')}
            >
              <Text style={[styles.langBtnText, lang === 'om' && styles.langBtnTextActive]}>AO</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      <View style={styles.searchRow}>
        <View style={styles.searchWrap}>
          <Ionicons name="search-outline" size={16} color={TEXT_MUTED} style={styles.searchIcon} />
          <TextInput
            ref={inputRef}
            style={styles.searchInput}
            placeholder={t('search_placeholder')}
            placeholderTextColor={TEXT_MUTED}
            value={query}
            onChangeText={setQuery}
            onSubmitEditing={handleSearch}
            returnKeyType="search"
          />
          {query.length > 0 && (
            <TouchableOpacity onPress={() => { setQuery(''); setSearch(''); setPage(1); }}>
              <Ionicons name="close-circle" size={16} color={TEXT_MUTED} />
            </TouchableOpacity>
          )}
        </View>
        <TouchableOpacity style={styles.searchBtn} onPress={handleSearch}>
          <Text style={styles.searchBtnText}>{t('search_btn')}</Text>
        </TouchableOpacity>
      </View>

      <ZoneFilter
        zones={zonesData || []}
        selected={zone}
        onSelect={handleZone}
        allZonesLabel={t('all_zones')}
      />

      {isLoading ? (
        <View style={styles.centered}>
          <ActivityIndicator color={ACCENT} size="large" />
          <Text style={styles.loadingText}>{t('loading')}</Text>
        </View>
      ) : legacies.length === 0 ? (
        <View style={styles.centered}>
          <Ionicons name="flame-outline" size={40} color={TEXT_MUTED} />
          <Text style={styles.emptyTitle}>{t('empty_title')}</Text>
          <Text style={styles.emptyText}>{t('empty_sub')}</Text>
        </View>
      ) : (
        <FlatList
          data={legacies}
          keyExtractor={(item) => String(item.id)}
          renderItem={({ item }) => (
            <LegacyCard
              item={item}
              onPress={() => router.push(`/legacy/${item.slug}` as any)}
              rememberedLabel={t('remembered')}
              readMoreLabel={t('read_more')}
            />
          )}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={isFetching && !isLoading}
              onRefresh={() => refetch()}
              tintColor={ACCENT}
            />
          }
          ListFooterComponent={
            hasMore ? (
              <TouchableOpacity
                style={styles.loadMoreBtn}
                onPress={() => setPage((p) => p + 1)}
              >
                <Text style={styles.loadMoreText}>{t('load_more')}</Text>
              </TouchableOpacity>
            ) : null
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: BG },
  header: {
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: BORDER,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
  },
  headerText: { flex: 1, marginRight: 12 },
  headerTitle: {
    fontSize: 24,
    fontWeight: '300',
    color: TEXT_PRIMARY,
    letterSpacing: 0.3,
  },
  headerSub: {
    fontSize: 13,
    color: TEXT_MUTED,
    marginTop: 2,
    fontStyle: 'italic',
  },
  langToggle: {
    flexDirection: 'row',
    borderWidth: 1,
    borderColor: '#3e2c12',
    borderRadius: 3,
    overflow: 'hidden',
    marginTop: 4,
  },
  langBtn: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    backgroundColor: 'transparent',
  },
  langBtnActive: { backgroundColor: ACCENT },
  langBtnText: { fontSize: 11, color: TEXT_MUTED, fontWeight: '700', letterSpacing: 0.5 },
  langBtnTextActive: { color: '#0e0a06' },
  searchRow: {
    flexDirection: 'row',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: SURFACE,
  },
  searchWrap: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#0b0803',
    borderWidth: 1,
    borderColor: '#3e2c12',
    borderRadius: 4,
    paddingHorizontal: 10,
    gap: 6,
  },
  searchIcon: { opacity: 0.7 },
  searchInput: {
    flex: 1,
    height: 38,
    color: TEXT_PRIMARY,
    fontSize: 14,
  },
  searchBtn: {
    backgroundColor: ACCENT,
    borderRadius: 4,
    paddingHorizontal: 16,
    justifyContent: 'center',
  },
  searchBtnText: {
    color: '#0e0a06',
    fontWeight: '700',
    fontSize: 13,
    letterSpacing: 0.5,
  },
  zoneList: { paddingHorizontal: 16, paddingVertical: 8, gap: 6 },
  zoneChip: {
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: 2,
    borderWidth: 1,
    borderColor: '#3e2c12',
    backgroundColor: CARD_BG,
    marginRight: 6,
  },
  zoneChipActive: {
    borderColor: ACCENT,
    backgroundColor: 'rgba(201,146,58,0.12)',
  },
  zoneChipText: { fontSize: 12, color: TEXT_MUTED, letterSpacing: 0.4 },
  zoneChipTextActive: { color: ACCENT, fontWeight: '600' },
  listContent: { padding: 16, gap: 12 },
  card: {
    backgroundColor: CARD_BG,
    borderWidth: 1,
    borderColor: BORDER,
    borderRadius: 2,
    overflow: 'hidden',
    marginBottom: 12,
  },
  cardAccentBar: {
    height: 2,
    backgroundColor: ACCENT,
    opacity: 0.4,
  },
  cardRow: {
    flexDirection: 'row',
    padding: 14,
    gap: 12,
  },
  cardPhotoWrap: {
    width: 68,
    height: 68,
    borderRadius: 2,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(201,146,58,0.2)',
  },
  cardPhoto: { width: '100%', height: '100%' },
  cardInitialWrap: {
    width: '100%',
    height: '100%',
    backgroundColor: '#120d05',
    alignItems: 'center',
    justifyContent: 'center',
  },
  cardInitial: { fontSize: 28, color: ACCENT, opacity: 0.55, fontWeight: '200' },
  cardContent: { flex: 1 },
  cardName: {
    fontSize: 17,
    fontWeight: '400',
    color: TEXT_PRIMARY,
    letterSpacing: 0.2,
    marginBottom: 2,
  },
  cardOccupation: {
    fontSize: 12,
    color: TEXT_SECONDARY,
    fontStyle: 'italic',
    marginBottom: 3,
  },
  cardZone: {
    fontSize: 10,
    color: ACCENT,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    marginBottom: 5,
  },
  cardStory: {
    fontSize: 13,
    color: TEXT_SECONDARY,
    lineHeight: 18,
    fontStyle: 'italic',
  },
  cardDate: {
    fontSize: 11,
    color: TEXT_MUTED,
    marginTop: 6,
    letterSpacing: 0.3,
  },
  cardFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: BORDER,
    backgroundColor: 'rgba(0,0,0,0.15)',
  },
  cardReadMore: {
    fontSize: 10,
    color: ACCENT,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    fontWeight: '600',
  },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 12, padding: 40 },
  loadingText: { color: TEXT_MUTED, fontSize: 14, fontStyle: 'italic' },
  emptyTitle: { fontSize: 18, color: TEXT_SECONDARY, fontStyle: 'italic' },
  emptyText: { fontSize: 13, color: TEXT_MUTED },
  loadMoreBtn: {
    alignSelf: 'center',
    marginTop: 8,
    marginBottom: 24,
    paddingHorizontal: 24,
    paddingVertical: 10,
    borderWidth: 1,
    borderColor: 'rgba(201,146,58,0.3)',
    borderRadius: 2,
  },
  loadMoreText: { color: ACCENT_LIGHT, fontSize: 13, letterSpacing: 0.5 },
});
