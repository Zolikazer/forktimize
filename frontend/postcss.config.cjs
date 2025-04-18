const purgecss = require('@fullhuman/postcss-purgecss').default;

const isProduction = process.env.NODE_ENV === 'production';

const config = {
    plugins: [
        ...(isProduction
            ? [
                purgecss({
                    content: ['./src/**/*.svelte', './index.html'],
                    defaultExtractor: (content) =>
                        content.match(/[\w-/:]+(?<!:)/g) || [],
                    safelist: [
                        /^is-/,
                        /^has-/,
                        /^level-/,
                        /^columns?/,
                        /^button/,
                        /^select/,
                        /^input/,
                        /^notification/,
                        'title',
                        'subtitle',
                        'container',
                        'content',
                    ],
                }),
            ]
            : []),
    ],
};
