import { describe, it, expect } from 'vitest';
import {translations} from "$lib/localisation/translations.js";

function flattenKeys(obj, prefix = '') {
    return Object.keys(obj).flatMap(key => {
        const fullKey = prefix ? `${prefix}.${key}` : key;
        if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
            return flattenKeys(obj[key], fullKey);
        }
        return fullKey;
    });
}

describe('Translations', () => {
    it('should have identical keys in all languages', () => {
        const enKeys = flattenKeys(translations.en);
        const huKeys = flattenKeys(translations.hu);

        expect(huKeys).toEqual(enKeys);
    });
});
