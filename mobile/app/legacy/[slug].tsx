import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  ActivityIndicator,
  Platform,
  TouchableOpacity,
  TextInput,
  KeyboardAvoidingView,
  Alert,
} from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import { fetchLegacy, fetchTributes, submitCandle, submitMessage } from '@/lib/api';
import { useLang } from '@/lib/lang';

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
const BORDER_LIGHT = '#3e2c12';
const ERROR = '#c97070';

function formatDate(str: string | null): string {
  if (!str) return '';
  const d = new Date(str);
  return d.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
}

function formatMessageDate(str: string): string {
  const d = new Date(str);
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

export default function LegacyDetailScreen() {
  const { slug } = useLocalSearchParams<{ slug: string }>();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const qc = useQueryClient();
  const { lang, t } = useLang();

  const [showMessageForm, setShowMessageForm] = useState(false);
  const [authorName, setAuthorName] = useState('');
  const [message, setMessage] = useState('');
  const [msgError, setMsgError] = useState('');

  const { data: legacy, isLoading, error } = useQuery({
    queryKey: ['legacy', slug],
    queryFn: () => fetchLegacy(slug!),
    enabled: !!slug,
  });

  const { data: tributes, refetch: refetchTributes } = useQuery({
    queryKey: ['tributes', slug],
    queryFn: () => fetchTributes(slug!),
    enabled: !!slug,
  });

  const candleMutation = useMutation({
    mutationFn: () => submitCandle(slug!),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['tributes', slug] });
    },
    onError: () => {
      Alert.alert('Error', 'Could not light candle. Please try again.');
    },
  });

  const messageMutation = useMutation({
    mutationFn: () => submitMessage(slug!, authorName.trim(), message.trim()),
    onSuccess: () => {
      setShowMessageForm(false);
      setAuthorName('');
      setMessage('');
      setMsgError('');
      qc.invalidateQueries({ queryKey: ['tributes', slug] });
    },
    onError: (err: any) => {
      setMsgError(err?.data?.message || err?.data?.detail || 'Could not send message. Please try again.');
    },
  });

  function handleSendMessage() {
    if (!message.trim()) {
      setMsgError('Please write a message before sending.');
      return;
    }
    messageMutation.mutate();
  }

  const botPad = Platform.OS === 'web' ? 34 : insets.bottom;

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={ACCENT} size="large" />
        <Text style={styles.loadingText}>{t('loading_story')}</Text>
      </View>
    );
  }

  if (error || !legacy) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorTitle}>{t('story_not_found')}</Text>
        <Text style={styles.errorText}>{t('story_pending')}</Text>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
          <Text style={styles.backBtnText}>{t('return_wall')}</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const initial = legacy.full_name?.charAt(0)?.toUpperCase() || '?';

  let displayStory = legacy.story;
  let storyNote: string | null = null;
  if (lang === 'om') {
    if (legacy.story_om && legacy.story_om.trim()) {
      displayStory = legacy.story_om;
    } else {
      displayStory = legacy.story_en || legacy.story;
      storyNote = t('no_story_om');
    }
  } else {
    displayStory = legacy.story_en || legacy.story;
  }

  const paragraphs = (displayStory || '').split('\n').filter((p: string) => p.trim());
  const candleCount = tributes?.candle_count ?? 0;
  const messages = tributes?.messages ?? [];

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: BG }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView
        style={styles.container}
        contentContainerStyle={{ paddingBottom: botPad + 32 }}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
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
            {legacy.occupation ? (
              <Text style={styles.heroOccupation}>{legacy.occupation}</Text>
            ) : null}
            {legacy.approved_at ? (
              <Text style={styles.heroDate}>{t('honored')} · {formatDate(legacy.approved_at)}</Text>
            ) : null}
          </View>
        </View>

        <View style={styles.storySection}>
          <View style={styles.storyDivider}>
            <View style={styles.dividerLine} />
            <Text style={styles.dividerLabel}>{t('their_story')}</Text>
            <View style={styles.dividerLine} />
          </View>

          {storyNote ? (
            <View style={styles.storyNote}>
              <Text style={styles.storyNoteText}>{storyNote}</Text>
            </View>
          ) : null}

          {paragraphs.map((para: string, i: number) => (
            <Text key={i} style={styles.paragraph}>{para}</Text>
          ))}

          <View style={[styles.storyDivider, { marginTop: 32 }]}>
            <View style={styles.dividerLine} />
            <Text style={{ color: ACCENT, fontSize: 10, opacity: 0.5 }}>✦</Text>
            <View style={styles.dividerLine} />
          </View>
        </View>

        <View style={styles.tributeSection}>
          <View style={styles.candleRow}>
            <Ionicons name="flame" size={18} color={ACCENT} style={{ opacity: 0.75 }} />
            <Text style={styles.candleCount}>
              {candleCount} {t('candles_lit')}
            </Text>
            <TouchableOpacity
              style={[styles.candleBtn, candleMutation.isPending && styles.btnDisabled]}
              onPress={() => candleMutation.mutate()}
              disabled={candleMutation.isPending}
              activeOpacity={0.75}
            >
              <Ionicons name="flame-outline" size={14} color="#0e0a06" />
              <Text style={styles.candleBtnText}>{t('light_candle')}</Text>
            </TouchableOpacity>
          </View>

          {!showMessageForm ? (
            <TouchableOpacity
              style={styles.leaveMessageBtn}
              onPress={() => setShowMessageForm(true)}
            >
              <Ionicons name="chatbubble-outline" size={14} color={ACCENT} />
              <Text style={styles.leaveMessageBtnText}>{t('leave_message')}</Text>
            </TouchableOpacity>
          ) : (
            <View style={styles.messageForm}>
              <TextInput
                style={styles.messageNameInput}
                placeholder={t('your_name')}
                placeholderTextColor={TEXT_MUTED}
                value={authorName}
                onChangeText={setAuthorName}
              />
              <TextInput
                style={[styles.messageInput, msgError ? styles.inputError : null]}
                placeholder={t('tribute_placeholder')}
                placeholderTextColor={TEXT_MUTED}
                value={message}
                onChangeText={(v) => { setMessage(v); setMsgError(''); }}
                multiline
                textAlignVertical="top"
              />
              {msgError ? <Text style={styles.inputErrorText}>{msgError}</Text> : null}
              <View style={styles.messageActions}>
                <TouchableOpacity
                  style={styles.cancelBtn}
                  onPress={() => { setShowMessageForm(false); setMessage(''); setAuthorName(''); setMsgError(''); }}
                >
                  <Text style={styles.cancelBtnText}>Cancel</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.sendBtn, messageMutation.isPending && styles.btnDisabled]}
                  onPress={handleSendMessage}
                  disabled={messageMutation.isPending}
                >
                  <Text style={styles.sendBtnText}>
                    {messageMutation.isPending ? t('sending') : t('submit_message')}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          )}

          {messages.length > 0 ? (
            <View style={styles.messagesSection}>
              <Text style={styles.messagesTitle}>{t('messages_left')}</Text>
              {messages.map((m) => (
                <View key={m.id} style={styles.messageCard}>
                  <View style={styles.messageHeader}>
                    <Text style={styles.messageAuthor}>
                      {m.author_name || 'Anonymous'}
                    </Text>
                    <Text style={styles.messageDate}>{formatMessageDate(m.created_at)}</Text>
                  </View>
                  <Text style={styles.messageText}>{m.message}</Text>
                </View>
              ))}
            </View>
          ) : null}
        </View>

        <View style={styles.sideCard}>
          <Text style={styles.sideCardTitle}>{t('in_remembrance')}</Text>
          <View style={styles.sideCardDivider} />
          <View style={styles.sideRow}>
            <Text style={styles.sideDt}>{t('name')}</Text>
            <Text style={styles.sideDd}>{legacy.full_name}</Text>
          </View>
          {legacy.zone_name ? (
            <View style={styles.sideRow}>
              <Text style={styles.sideDt}>{t('region')}</Text>
              <Text style={styles.sideDd}>{legacy.zone_name}, {t('oromiyaa')}</Text>
            </View>
          ) : null}
          {legacy.approved_at ? (
            <View style={styles.sideRow}>
              <Text style={styles.sideDt}>{t('honored')}</Text>
              <Text style={styles.sideDd}>{formatDate(legacy.approved_at)}</Text>
            </View>
          ) : null}
        </View>

        <TouchableOpacity style={styles.returnBtn} onPress={() => router.back()}>
          <Text style={styles.returnBtnText}>{t('return_wall')}</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
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
    marginBottom: 4,
  },
  heroOccupation: {
    fontSize: 13,
    color: TEXT_SECONDARY,
    fontStyle: 'italic',
    marginBottom: 6,
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
  storyNote: {
    backgroundColor: 'rgba(201,146,58,0.06)',
    borderLeftWidth: 2,
    borderLeftColor: 'rgba(201,146,58,0.3)',
    padding: 10,
    marginBottom: 16,
    borderRadius: 2,
  },
  storyNoteText: { fontSize: 12, color: TEXT_MUTED, fontStyle: 'italic' },
  paragraph: {
    fontSize: 16,
    color: TEXT_BODY,
    lineHeight: 26,
    marginBottom: 16,
  },
  tributeSection: {
    marginHorizontal: 20,
    marginBottom: 16,
    backgroundColor: CARD_BG,
    borderWidth: 1,
    borderColor: BORDER,
    borderTopWidth: 2,
    borderTopColor: 'rgba(201,146,58,0.25)',
    padding: 16,
    borderRadius: 2,
  },
  candleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  candleCount: {
    flex: 1,
    fontSize: 13,
    color: TEXT_SECONDARY,
    fontStyle: 'italic',
  },
  candleBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    backgroundColor: ACCENT,
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: 3,
  },
  candleBtnText: { color: '#0e0a06', fontSize: 12, fontWeight: '700', letterSpacing: 0.3 },
  leaveMessageBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: BORDER,
  },
  leaveMessageBtnText: { color: ACCENT, fontSize: 13, letterSpacing: 0.3 },
  messageForm: {
    marginTop: 4,
    borderTopWidth: 1,
    borderTopColor: BORDER,
    paddingTop: 12,
    gap: 8,
  },
  messageNameInput: {
    backgroundColor: '#0b0803',
    borderWidth: 1,
    borderColor: BORDER_LIGHT,
    borderRadius: 3,
    paddingHorizontal: 12,
    paddingVertical: 8,
    color: TEXT_PRIMARY,
    fontSize: 14,
  },
  messageInput: {
    backgroundColor: '#0b0803',
    borderWidth: 1,
    borderColor: BORDER_LIGHT,
    borderRadius: 3,
    paddingHorizontal: 12,
    paddingVertical: 8,
    color: TEXT_PRIMARY,
    fontSize: 14,
    minHeight: 80,
  },
  inputError: { borderColor: ERROR },
  inputErrorText: { fontSize: 12, color: ERROR, marginTop: 2 },
  messageActions: { flexDirection: 'row', gap: 8, justifyContent: 'flex-end' },
  cancelBtn: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderWidth: 1,
    borderColor: BORDER_LIGHT,
    borderRadius: 3,
  },
  cancelBtnText: { color: TEXT_MUTED, fontSize: 13 },
  sendBtn: {
    backgroundColor: ACCENT,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 3,
  },
  sendBtnText: { color: '#0e0a06', fontSize: 13, fontWeight: '700' },
  btnDisabled: { opacity: 0.55 },
  messagesSection: {
    marginTop: 16,
    borderTopWidth: 1,
    borderTopColor: BORDER,
    paddingTop: 12,
    gap: 8,
  },
  messagesTitle: {
    fontSize: 9,
    color: TEXT_MUTED,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    fontWeight: '700',
    marginBottom: 6,
  },
  messageCard: {
    backgroundColor: '#0e0a06',
    borderWidth: 1,
    borderColor: BORDER,
    borderRadius: 2,
    padding: 10,
    marginBottom: 6,
  },
  messageHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 6 },
  messageAuthor: { fontSize: 12, color: ACCENT_LIGHT, fontWeight: '600' },
  messageDate: { fontSize: 10, color: TEXT_MUTED, fontStyle: 'italic' },
  messageText: { fontSize: 14, color: TEXT_BODY, lineHeight: 20, fontStyle: 'italic' },
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
