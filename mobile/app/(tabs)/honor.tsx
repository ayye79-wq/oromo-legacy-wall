import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  Alert,
  Platform,
  KeyboardAvoidingView,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { useQuery } from '@tanstack/react-query';
import { fetchZones, submitLegacy, Zone } from '@/lib/api';
import { useLang } from '@/lib/lang';

const ACCENT = '#c9923a';
const BG = '#0e0a06';
const CARD_BG = '#1a1208';
const SURFACE = '#130d07';
const TEXT_PRIMARY = '#f0e6d0';
const TEXT_SECONDARY = '#b8956a';
const TEXT_MUTED = '#7a5e3a';
const BORDER = '#2c1e0a';
const BORDER_LIGHT = '#3e2c12';
const ERROR = '#c97070';

type StoryLang = 'en' | 'om' | 'both';

export default function HonorScreen() {
  const insets = useSafeAreaInsets();
  const { lang, t } = useLang();

  const [fullName, setFullName] = useState('');
  const [occupation, setOccupation] = useState('');
  const [zoneId, setZoneId] = useState('');
  const [storyLang, setStoryLang] = useState<StoryLang>('en');
  const [storyEn, setStoryEn] = useState('');
  const [storyOm, setStoryOm] = useState('');
  const [photo, setPhoto] = useState<{ uri: string; name: string; type: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [showZones, setShowZones] = useState(false);

  const { data: zones = [] } = useQuery({ queryKey: ['zones'], queryFn: fetchZones });

  const selectedZone = zones.find((z) => String(z.id) === zoneId);

  async function pickPhoto() {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [3, 4],
      quality: 0.8,
    });
    if (!result.canceled && result.assets[0]) {
      const asset = result.assets[0];
      const ext = asset.uri.split('.').pop() || 'jpg';
      setPhoto({
        uri: asset.uri,
        name: `portrait.${ext}`,
        type: `image/${ext}`,
      });
    }
  }

  function validate() {
    const errs: Record<string, string> = {};
    if (!fullName.trim()) errs.full_name = t('err_name');
    if (!zoneId) errs.zone = t('err_zone');
    const enTrimmed = storyEn.trim();
    const omTrimmed = storyOm.trim();
    if (storyLang === 'en' && !enTrimmed) errs.story_en = t('err_story');
    else if (storyLang === 'en' && enTrimmed.length < 30) errs.story_en = t('err_story_short');
    if (storyLang === 'om' && !omTrimmed) errs.story_om = t('err_story');
    else if (storyLang === 'om' && omTrimmed.length < 30) errs.story_om = t('err_story_short');
    if (storyLang === 'both') {
      if (!enTrimmed && !omTrimmed) errs.story_en = t('err_story');
      else if (enTrimmed && enTrimmed.length < 30) errs.story_en = t('err_story_short');
      else if (omTrimmed && omTrimmed.length < 30) errs.story_om = t('err_story_short');
    }
    return errs;
  }

  async function handleSubmit() {
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    setSubmitting(true);
    setErrors({});

    const fd = new FormData();
    fd.append('full_name', fullName.trim());
    if (occupation.trim()) fd.append('occupation', occupation.trim());
    fd.append('zone', zoneId);
    fd.append('original_language', storyLang === 'both' ? 'both' : storyLang);

    if (storyLang === 'en' || storyLang === 'both') {
      if (storyEn.trim()) fd.append('story_en', storyEn.trim());
    }
    if (storyLang === 'om' || storyLang === 'both') {
      if (storyOm.trim()) fd.append('story_om', storyOm.trim());
    }
    const primaryStory = storyEn.trim() || storyOm.trim();
    fd.append('story', primaryStory);

    if (photo) {
      fd.append('photo', { uri: photo.uri, name: photo.name, type: photo.type } as any);
    }

    try {
      await submitLegacy(fd);
      setSuccess(true);
      setFullName('');
      setOccupation('');
      setZoneId('');
      setStoryEn('');
      setStoryOm('');
      setPhoto(null);
    } catch (err: any) {
      if (err.data) {
        const apiErrs: Record<string, string> = {};
        Object.entries(err.data).forEach(([k, v]) => {
          apiErrs[k] = Array.isArray(v) ? (v as string[]).join(' ') : String(v);
        });
        setErrors(apiErrs);
      } else {
        Alert.alert('Error', 'Something went wrong. Please try again.');
      }
    }
    setSubmitting(false);
  }

  const topPad = Platform.OS === 'web' ? 67 : insets.top;
  const botPad = Platform.OS === 'web' ? 34 : insets.bottom;

  if (success) {
    return (
      <View style={[styles.container, { paddingTop: topPad }]}>
        <View style={styles.successWrap}>
          <Ionicons name="flame" size={48} color={ACCENT} style={{ opacity: 0.7, marginBottom: 20 }} />
          <Text style={styles.successTitle}>{t('success_title')}</Text>
          <View style={styles.successDivider} />
          <Text style={styles.successText}>{t('success_body')}</Text>
          <TouchableOpacity style={styles.successBtn} onPress={() => setSuccess(false)}>
            <Text style={styles.successBtnText}>{t('honor_another')}</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  const showEnField = storyLang === 'en' || storyLang === 'both';
  const showOmField = storyLang === 'om' || storyLang === 'both';
  const enChars = storyEn.length;
  const omChars = storyOm.length;

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: BG }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={[styles.container, { paddingTop: topPad }]}>
        <View style={styles.header}>
          <Text style={styles.headerKicker}>{t('honor_kicker')}</Text>
          <Text style={styles.headerTitle}>{t('honor_title')}</Text>
        </View>

        <ScrollView
          contentContainerStyle={[styles.formContent, { paddingBottom: botPad + 32 }]}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>{t('who_honoring')}</Text>

            <View style={styles.field}>
              <Text style={styles.label}>{t('full_name_label')} <Text style={styles.required}>*</Text></Text>
              <TextInput
                style={[styles.input, errors.full_name ? styles.inputError : null]}
                placeholder="Their full name…"
                placeholderTextColor={TEXT_MUTED}
                value={fullName}
                onChangeText={(v) => { setFullName(v); setErrors((e) => ({ ...e, full_name: '' })); }}
              />
              {errors.full_name ? <Text style={styles.errorText}>{errors.full_name}</Text> : null}
            </View>

            <View style={styles.field}>
              <Text style={styles.label}>{t('role_label')} <Text style={styles.optional}>(optional)</Text></Text>
              <TextInput
                style={styles.input}
                placeholder={t('role_placeholder')}
                placeholderTextColor={TEXT_MUTED}
                value={occupation}
                onChangeText={setOccupation}
              />
              <Text style={styles.helpText}>{t('role_help')}</Text>
            </View>

            <View style={styles.field}>
              <Text style={styles.label}>{t('zone_label')} <Text style={styles.required}>*</Text></Text>
              <TouchableOpacity
                style={[styles.input, styles.selectInput, errors.zone ? styles.inputError : null]}
                onPress={() => setShowZones(!showZones)}
              >
                <Text style={selectedZone ? styles.inputText : styles.placeholderText}>
                  {selectedZone?.name || t('zone_placeholder')}
                </Text>
                <Ionicons name={showZones ? 'chevron-up' : 'chevron-down'} size={14} color={TEXT_MUTED} />
              </TouchableOpacity>
              {showZones && (
                <View style={styles.zoneDropdown}>
                  {zones.map((z) => (
                    <TouchableOpacity
                      key={z.id}
                      style={[styles.zoneOption, String(z.id) === zoneId && styles.zoneOptionActive]}
                      onPress={() => { setZoneId(String(z.id)); setShowZones(false); setErrors((e) => ({ ...e, zone: '' })); }}
                    >
                      <Text style={[styles.zoneOptionText, String(z.id) === zoneId && styles.zoneOptionTextActive]}>
                        {z.name}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              )}
              {errors.zone ? <Text style={styles.errorText}>{errors.zone}</Text> : null}
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>{t('story_section')}</Text>
            <Text style={styles.sectionNote}>{t('story_note')}</Text>

            <View style={styles.field}>
              <Text style={styles.label}>{t('story_lang_label')}</Text>
              <View style={styles.storyLangRow}>
                {(['en', 'om', 'both'] as StoryLang[]).map((opt) => {
                  const labels = { en: t('story_lang_en'), om: t('story_lang_om'), both: t('story_lang_both') };
                  return (
                    <TouchableOpacity
                      key={opt}
                      style={[styles.storyLangChip, storyLang === opt && styles.storyLangChipActive]}
                      onPress={() => setStoryLang(opt)}
                    >
                      <Text style={[styles.storyLangChipText, storyLang === opt && styles.storyLangChipTextActive]}>
                        {labels[opt]}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>

            {showEnField && (
              <View style={styles.field}>
                <Text style={styles.label}>{t('story_en_label')} <Text style={styles.required}>*</Text></Text>
                <TextInput
                  style={[styles.input, styles.textArea, errors.story_en ? styles.inputError : null]}
                  placeholder={t('story_placeholder_en')}
                  placeholderTextColor={TEXT_MUTED}
                  value={storyEn}
                  onChangeText={(v) => { setStoryEn(v); setErrors((e) => ({ ...e, story_en: '' })); }}
                  multiline
                  textAlignVertical="top"
                />
                {errors.story_en ? <Text style={styles.errorText}>{errors.story_en}</Text> : null}
                <Text style={styles.helpText}>{enChars} {t('chars_written')}</Text>
              </View>
            )}

            {showOmField && (
              <View style={styles.field}>
                <Text style={styles.label}>{t('story_om_label')} <Text style={styles.required}>*</Text></Text>
                <TextInput
                  style={[styles.input, styles.textArea, errors.story_om ? styles.inputError : null]}
                  placeholder={t('story_placeholder_om')}
                  placeholderTextColor={TEXT_MUTED}
                  value={storyOm}
                  onChangeText={(v) => { setStoryOm(v); setErrors((e) => ({ ...e, story_om: '' })); }}
                  multiline
                  textAlignVertical="top"
                />
                {errors.story_om ? <Text style={styles.errorText}>{errors.story_om}</Text> : null}
                <Text style={styles.helpText}>{omChars} {t('chars_written')}</Text>
              </View>
            )}
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>{t('photo_section')} <Text style={styles.optional}>(optional)</Text></Text>

            {photo ? (
              <View style={styles.photoPreview}>
                <Image source={{ uri: photo.uri }} style={styles.previewImage} />
                <TouchableOpacity style={styles.removePhoto} onPress={() => setPhoto(null)}>
                  <Ionicons name="close" size={16} color={TEXT_PRIMARY} />
                </TouchableOpacity>
              </View>
            ) : (
              <TouchableOpacity style={styles.photoBtn} onPress={pickPhoto}>
                <Ionicons name="image-outline" size={20} color={TEXT_MUTED} />
                <Text style={styles.photoBtnText}>{t('choose_photo')}</Text>
              </TouchableOpacity>
            )}
          </View>

          {errors._general ? (
            <View style={styles.errorBanner}>
              <Text style={styles.errorBannerText}>{errors._general}</Text>
            </View>
          ) : null}

          <TouchableOpacity
            style={[styles.submitBtn, submitting && styles.submitBtnDisabled]}
            onPress={handleSubmit}
            disabled={submitting}
            activeOpacity={0.8}
          >
            {submitting ? (
              <ActivityIndicator color="#0e0a06" size="small" />
            ) : null}
            <Text style={styles.submitBtnText}>
              {submitting ? t('submitting') : t('submit_btn')}
            </Text>
          </TouchableOpacity>
        </ScrollView>
      </View>
    </KeyboardAvoidingView>
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
  headerKicker: { fontSize: 10, color: ACCENT, letterSpacing: 0.3, opacity: 0.7, textTransform: 'uppercase', marginBottom: 4 },
  headerTitle: { fontSize: 26, fontWeight: '300', color: TEXT_PRIMARY, letterSpacing: 0.3 },
  formContent: { padding: 16 },
  section: {
    backgroundColor: CARD_BG,
    borderWidth: 1,
    borderColor: BORDER,
    borderTopWidth: 2,
    borderTopColor: 'rgba(201,146,58,0.3)',
    padding: 16,
    marginBottom: 12,
    borderRadius: 2,
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: TEXT_PRIMARY,
    marginBottom: 4,
    letterSpacing: 0.2,
  },
  sectionNote: { fontSize: 12, color: TEXT_MUTED, fontStyle: 'italic', marginBottom: 14 },
  field: { marginBottom: 14 },
  label: {
    fontSize: 10,
    fontWeight: '700',
    color: TEXT_MUTED,
    letterSpacing: 0.8,
    marginBottom: 6,
    textTransform: 'uppercase',
  },
  required: { color: ACCENT },
  optional: { fontWeight: '400', color: TEXT_MUTED, textTransform: 'none', letterSpacing: 0, fontSize: 11 },
  input: {
    backgroundColor: '#0b0803',
    borderWidth: 1,
    borderColor: BORDER_LIGHT,
    borderRadius: 3,
    paddingHorizontal: 12,
    paddingVertical: 10,
    color: TEXT_PRIMARY,
    fontSize: 15,
  },
  inputText: { color: TEXT_PRIMARY, fontSize: 15, flex: 1 },
  placeholderText: { color: TEXT_MUTED, fontSize: 15, fontStyle: 'italic', flex: 1 },
  inputError: { borderColor: ERROR },
  selectInput: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  textArea: { minHeight: 140, paddingTop: 10 },
  errorText: { fontSize: 12, color: ERROR, marginTop: 4 },
  helpText: { fontSize: 11, color: TEXT_MUTED, marginTop: 4, fontStyle: 'italic' },
  storyLangRow: { flexDirection: 'row', gap: 6, flexWrap: 'wrap' },
  storyLangChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 3,
    borderWidth: 1,
    borderColor: BORDER_LIGHT,
    backgroundColor: '#0b0803',
  },
  storyLangChipActive: {
    borderColor: ACCENT,
    backgroundColor: 'rgba(201,146,58,0.12)',
  },
  storyLangChipText: { fontSize: 13, color: TEXT_MUTED },
  storyLangChipTextActive: { color: ACCENT, fontWeight: '600' },
  zoneDropdown: {
    backgroundColor: '#0b0803',
    borderWidth: 1,
    borderColor: BORDER_LIGHT,
    borderRadius: 3,
    marginTop: 2,
    maxHeight: 200,
    overflow: 'hidden',
  },
  zoneOption: { paddingHorizontal: 12, paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: BORDER },
  zoneOptionActive: { backgroundColor: 'rgba(201,146,58,0.08)' },
  zoneOptionText: { fontSize: 14, color: TEXT_SECONDARY },
  zoneOptionTextActive: { color: ACCENT },
  photoBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    padding: 14,
    backgroundColor: '#0b0803',
    borderWidth: 1,
    borderStyle: 'dashed',
    borderColor: BORDER_LIGHT,
    borderRadius: 3,
  },
  photoBtnText: { color: TEXT_MUTED, fontSize: 14, fontStyle: 'italic' },
  photoPreview: { position: 'relative', alignSelf: 'flex-start' },
  previewImage: { width: 120, height: 160, borderRadius: 2 },
  removePhoto: {
    position: 'absolute',
    top: 6,
    right: 6,
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 12,
    padding: 4,
  },
  errorBanner: {
    backgroundColor: 'rgba(201,112,112,0.08)',
    borderWidth: 1,
    borderColor: 'rgba(201,112,112,0.25)',
    padding: 12,
    borderRadius: 3,
    marginBottom: 12,
  },
  errorBannerText: { color: '#d9958e', fontSize: 14 },
  submitBtn: {
    backgroundColor: ACCENT,
    borderRadius: 3,
    paddingVertical: 14,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    marginTop: 8,
  },
  submitBtnDisabled: { opacity: 0.6 },
  submitBtnText: { color: '#0e0a06', fontSize: 15, fontWeight: '700', letterSpacing: 0.3 },
  successWrap: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  successTitle: {
    fontSize: 22,
    fontWeight: '300',
    color: TEXT_PRIMARY,
    textAlign: 'center',
    letterSpacing: 0.3,
    marginBottom: 16,
  },
  successDivider: {
    width: 60,
    height: 1,
    backgroundColor: ACCENT,
    opacity: 0.4,
    marginBottom: 20,
  },
  successText: {
    fontSize: 15,
    color: TEXT_SECONDARY,
    textAlign: 'center',
    lineHeight: 24,
    fontStyle: 'italic',
    marginBottom: 32,
  },
  successBtn: {
    borderWidth: 1,
    borderColor: 'rgba(201,146,58,0.3)',
    borderRadius: 3,
    paddingVertical: 12,
    paddingHorizontal: 24,
  },
  successBtnText: { color: ACCENT, fontSize: 14, letterSpacing: 0.5 },
});
