import React, { useState, useEffect } from 'react';
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

export default function HonorScreen() {
  const insets = useSafeAreaInsets();
  const [fullName, setFullName] = useState('');
  const [zoneId, setZoneId] = useState('');
  const [story, setStory] = useState('');
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
    if (!fullName.trim()) errs.full_name = 'Their full name is required.';
    if (!zoneId) errs.zone = 'Please select a zone.';
    if (!story.trim()) errs.story = 'Please share their story.';
    if (story.trim().length < 30) errs.story = 'Please write a little more — at least 30 characters.';
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
    fd.append('zone', zoneId);
    fd.append('story', story.trim());
    if (photo) {
      fd.append('photo', { uri: photo.uri, name: photo.name, type: photo.type } as any);
    }

    try {
      await submitLegacy(fd);
      setSuccess(true);
      setFullName('');
      setZoneId('');
      setStory('');
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
          <Text style={styles.successTitle}>Their Story Has Been Received</Text>
          <View style={styles.successDivider} />
          <Text style={styles.successText}>
            Your tribute has been received. A community moderator will review it
            carefully before it appears on the Memorial Wall. Thank you for
            preserving this life for generations to come.
          </Text>
          <TouchableOpacity style={styles.successBtn} onPress={() => setSuccess(false)}>
            <Text style={styles.successBtnText}>Honor Another Life</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: BG }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={[styles.container, { paddingTop: topPad }]}>
        <View style={styles.header}>
          <Text style={styles.headerKicker}>In Their Memory</Text>
          <Text style={styles.headerTitle}>Honor a Life</Text>
        </View>

        <ScrollView
          contentContainerStyle={[styles.formContent, { paddingBottom: botPad + 32 }]}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Who Are You Honoring?</Text>

            <View style={styles.field}>
              <Text style={styles.label}>FULL NAME <Text style={styles.required}>*</Text></Text>
              <TextInput
                style={[styles.input, errors.full_name ? styles.inputError : null]}
                placeholder="Their full name…"
                placeholderTextColor={TEXT_MUTED}
                value={fullName}
                onChangeText={(t) => { setFullName(t); setErrors((e) => ({ ...e, full_name: '' })); }}
              />
              {errors.full_name ? <Text style={styles.errorText}>{errors.full_name}</Text> : null}
            </View>

            <View style={styles.field}>
              <Text style={styles.label}>ZONE OF OROMIYAA <Text style={styles.required}>*</Text></Text>
              <TouchableOpacity
                style={[styles.input, styles.selectInput, errors.zone ? styles.inputError : null]}
                onPress={() => setShowZones(!showZones)}
              >
                <Text style={selectedZone ? styles.inputText : styles.placeholderText}>
                  {selectedZone?.name || 'Select their zone…'}
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
            <Text style={styles.sectionTitle}>Their Story</Text>
            <Text style={styles.sectionNote}>
              Share who they were, what they meant to you, their life and legacy.
            </Text>
            <View style={styles.field}>
              <Text style={styles.label}>BIOGRAPHY &amp; STORY <Text style={styles.required}>*</Text></Text>
              <TextInput
                style={[styles.input, styles.textArea, errors.story ? styles.inputError : null]}
                placeholder="In the words of those who loved them…"
                placeholderTextColor={TEXT_MUTED}
                value={story}
                onChangeText={(t) => { setStory(t); setErrors((e) => ({ ...e, story: '' })); }}
                multiline
                textAlignVertical="top"
              />
              {errors.story ? <Text style={styles.errorText}>{errors.story}</Text> : null}
              <Text style={styles.helpText}>{story.length} characters written</Text>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>A Portrait <Text style={styles.optional}>(optional)</Text></Text>

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
                <Text style={styles.photoBtnText}>Choose a photograph…</Text>
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
              {submitting ? 'Preserving their memory…' : 'Place Their Story on the Wall'}
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
  optional: { fontWeight: '400', color: TEXT_MUTED, textTransform: 'none', letterSpacing: 0, fontSize: 12 },
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
  textArea: { minHeight: 160, paddingTop: 10 },
  errorText: { fontSize: 12, color: ERROR, marginTop: 4 },
  helpText: { fontSize: 11, color: TEXT_MUTED, marginTop: 4, fontStyle: 'italic' },
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
