import pandas as pd
import numpy as np

def read_csv_file():
    try:
        # Читаем CSV файл
        df = pd.read_csv('train.csv')
        return df
    except FileNotFoundError:
        print("Ошибка: Файл train.csv не найден")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {str(e)}")
        return None

def analyze_gender_distribution(df):
    gender_counts = df['Sex'].value_counts()
    print("\n1. Количество мужчин и женщин на борту:")
    print(f"Мужчины: {gender_counts['male']}")
    print(f"Женщины: {gender_counts['female']}")

def analyze_embarkation_ports(df):
    port_counts = df['Embarked'].value_counts()
    print("\n2. Количество пассажиров по портам посадки:")
    print(f"{port_counts['S']} {port_counts['C']} {port_counts['Q']}")

def analyze_survival_rate(df):
    total_passengers = len(df)
    deceased = df['Survived'].value_counts()[0]
    survival_rate = (deceased / total_passengers) * 100
    print("\n3. Количество и процент погибших:")
    print(f"Количество погибших: {deceased}")
    print(f"Процент погибших: {survival_rate:.2f}%")

def analyze_class_distribution(df):
    class_distribution = df['Pclass'].value_counts(normalize=True) * 100
    print("\n4. Доли пассажиров по классам:")
    for pclass in sorted(class_distribution.index):
        print(f"Класс {pclass}: {class_distribution[pclass]:.2f}%")
    

def calculate_correlation(df):
    correlation = df['SibSp'].corr(df['Parch'])
    print("\n5. Коэффициент корреляции Пирсона между SibSp и Parch:")
    print(f"{correlation:.4f}")

def analyze_survival_correlations(df):
    # Корреляция между возрастом и выживаемостью
    age_corr = df['Age'].corr(df['Survived'])
    
    # Для корреляции с полом нужно преобразовать его в числовой формат
    df['Sex_numeric'] = df['Sex'].map({'male': 0, 'female': 1})
    sex_corr = df['Sex_numeric'].corr(df['Survived'])
    class_corr = df['Pclass'].corr(df['Survived'])
    print("\n6.Доп корреляция")
    print(f"Корреляция возраст-выживаемость: {age_corr:.4f}")  # Показывает связь между возрастом и выживаемостью
    print(f"Корреляция пол-выживаемость: {sex_corr:.4f}")      # Показывает связь между полом и выживаемостью 
    print(f"Корреляция класс-выживаемость: {class_corr:.4f}")  # Показывает связь между классом и выживаемостью

def analyze_age_statistics(df):
    mean_age = df['Age'].mean()
    median_age = df['Age'].median()
    min_age = df['Age'].min()
    max_age = df['Age'].max()
    print("\n7.Статистика по возрасту:")
    print(f"Средний возраст - {mean_age:.2f}")
    print(f"Медианный возраст - {median_age:.2f}")
    print(f"Минимальный возраст - {min_age:.2f}")
    print(f"Максимальный возраст - {max_age:.2f}")

def analyze_fare_statistics(df):
    mean_fare = df['Fare'].mean()
    median_fare = df['Fare'].median()
    min_fare = df['Fare'].min()
    max_fare = df['Fare'].max()
    print("\n8.Статистика по ценам билетов:")
    print(f"Средняя цена - {mean_fare:.2f}")
    print(f"Медианная цена - {median_fare:.2f}")
    print(f"Минимальная цена - {min_fare:.2f}")
    print(f"Максимальная цена - {max_fare:.2f}")

def extract_male_first_name(name):
    # Извлекаем первое имя из полного имени для мужчин
    try:
        # Убираем фамилию и титул (Mr., etc.)
        name = name.split(',')[1].strip()
        # Убираем титул в скобках если есть
        if '(' in name:
            name = name.split('(')[0].strip()
        # Берем следующее слово после титула Mr.
        if 'Mr.' in name:
            name = name.split('Mr.')[1].strip().split()[0]
        else:
            name = name.split()[1]
        return name
    except:
        return None

def extract_female_first_name(name):
    # Извлекаем первое имя из полного имени для женщин
    try:
        # Убираем фамилию
        name = name.split(',')[1].strip()
        
        # Для замужних женщин (Mrs.)
        if 'Mrs.' in name:
            # Берем имя в скобках если есть
            if '(' in name:
                name = name.split('(')[1].split(')')[0].strip()
                # Берем первое слово из имени в скобках
                name = name.split(' ')[0].strip()
            else:
                name = name.split('Mrs.')[1].strip()
                name = name.split(' ')[0].strip()
                
        # Для незамужних женщин (Miss.)
        elif 'Miss.' in name:
            name = name.split('Miss.')[1].strip()
            name = name.split(' ')[0].strip()
            
        # Для Ms.
        elif 'Ms.' in name:
            name = name.split('Ms.')[1].strip()
            name = name.split(' ')[0].strip()
            
        else:
            name = name.split(' ')[1].strip()
            
        return name
    except:
        return None

def analyze_popular_male_name(df):
    # Фильтруем только мужчин
    male_df = df[df['Sex'] == 'male'].copy()
    male_df['FirstName'] = male_df['Name'].apply(extract_male_first_name)
    name_counts = male_df['FirstName'].value_counts()
    most_common_name_male = name_counts.index[0]
    count_male = name_counts.iloc[0]
    print("\n9.Самое популярное мужское имя:")
    print(f"{most_common_name_male} (количество: {count_male})")

def analyze_popular_female_name(df):
    # Сначала фильтруем по возрасту старше 15 лет
    df15 = df[df['Age'] > 15].copy()
    
    # Затем фильтруем женщин
    female_df15 = df15[df15['Sex'] == 'female'].copy()
    female_df15['FirstName'] = female_df15['Name'].apply(extract_female_first_name)
    name_counts = female_df15['FirstName'].value_counts()
    most_common_name_female15 = name_counts.index[0]
    count_female15 = name_counts.iloc[0]

    # Фильтруем мужчин
    male_df15 = df15[df15['Sex'] == 'male'].copy()
    male_df15['FirstName'] = male_df15['Name'].apply(extract_male_first_name)
    name_counts = male_df15['FirstName'].value_counts()
    most_common_name_male15 = name_counts.index[0]
    count_male15 = name_counts.iloc[0]

    print("\n10.1 Самое популярное женское имя >15 лет:")
    print(f"{most_common_name_female15} (количество: {count_female15})")
    print("\n10.2 Самое популярное мужское имя >15 лет:")
    print(f"{most_common_name_male15} (количество: {count_male15})")

if __name__ == "__main__":
    df = read_csv_file()
    if df is not None:
        analyze_gender_distribution(df)
        analyze_embarkation_ports(df)
        analyze_survival_rate(df)
        analyze_class_distribution(df)
        calculate_correlation(df)
        analyze_survival_correlations(df)
        analyze_age_statistics(df)
        analyze_fare_statistics(df)
        analyze_popular_male_name(df)
        analyze_popular_female_name(df)
