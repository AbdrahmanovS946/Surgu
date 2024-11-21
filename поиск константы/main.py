import matplotlib.pyplot as plt

def text_replacing(text):
    text = text.lower()
    for i in 'qwertyuiopasdfghjklzxcvbnm1234567890«~.,…—-–”“?!#№&_=+\|/:;<>()[]}{%$@^*"':
        text = text.replace(i, " ")
    return text

def zipf_law_analysis(text):
    word_frequencies = {}
    total_word_count = 0

    with open(text, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        content = text_replacing(text)
        words = content.split()
        total_word_count = len(words)

    total_word_count = len(words)
    for word in words:
        if word in word_frequencies:
            word_frequencies[word] += 1
        else:
            word_frequencies[word] = 1

    sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)

    current_constant = 1

    while True:
        next_constant = current_constant + 1
        current_sum = 0
        next_sum = 0
        rank = 1

        for word, experimental_point in sorted_word_frequencies:
            current_theoretical_point = round(current_constant / rank, 0)
            next_theoretical_point = round(next_constant / rank, 0)

            current_sum += pow(experimental_point - current_theoretical_point, 2)
            next_sum += pow(experimental_point - next_theoretical_point, 2)

            rank += 1

        current_constant = next_constant

        if next_sum > current_sum:
            break

    rank_values = []
    experimental_frequencies = []
    theoretical_frequencies = []

    for rank, (word, experimental_point) in enumerate(sorted_word_frequencies, start=1):
        word_frequency = experimental_point / total_word_count
        rank_values.append(rank)
        experimental_frequencies.append(word_frequency)

        theoretical_point = current_constant / rank

        theoretical_frequency = theoretical_point / total_word_count
        theoretical_frequencies.append(theoretical_frequency)

    TOP_ROWS = 100
    
    print("Rank. Frequency. Word. Test. Theory.")
    for i in range(TOP_ROWS):
        print(f"[Rank: {rank_values[i]}] Frequency: {experimental_frequencies[i]} | Word: {sorted_word_frequencies[i][0]}, Test: {sorted_word_frequencies[i][1]} | Theory: {theoretical_frequencies[i]}")

    real_constant = rank_values[-1] * experimental_frequencies[-1]
    print(f'Constant: {current_constant}')
    print(f'Real Constant: {real_constant}')

    plt.plot(rank_values, experimental_frequencies, marker='o', label='Experimental Data')
    plt.plot(rank_values, theoretical_frequencies, label='Theoretical Data', linestyle='--')
    plt.title('Word Frequency by Rank')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()
    
file = r'C:\Users\sergey\Desktop\поиск константы\литература\Ник_Бостром_Искусственный_интеллект.txt'

zipf_law_analysis(file)