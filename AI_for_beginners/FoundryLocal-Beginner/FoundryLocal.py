from foundry_local_sdk import Configuration, FoundryLocalManager

"""
Ne yapıyor? Microsoft Foundry Yerel SDK'sından iki temel sınıfı projemize dahil ediyor.
Neden yazdık? * Configuration: Yapay zeka motorunun hangi ayarlarla (örneğin hangi donanımı kullanacağı, önbellek klasörleri vb.) çalışacağını belirlemek için kullanılır.
FoundryLocalManager: Yapay zeka modelini indiren, hafızaya yükleyen ve yöneten ana orkestra şefidir.
"""

def main():
    # Initialize the Foundry Local SDK
    config = Configuration(app_name="foundry_local_samples")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    """
    Ne yapıyor? Programın giriş noktasını (main) oluşturuyor. foundry_local_samples adında bir uygulama profili tanımlayarak SDK'yı ayağa kaldırıyor ve bu motorun bir örneğini (instance) manager değişkenine atıyor.
    Neden yazdık? Yapay zeka modelini yüklemeden önce arkadaki ana motoru çalıştırmamız gerekir. manager üzerinden tüm model indirme ve yükleme işlemlerini kontrol edeceğiz.
    """


    # Download and register all execution providers.
    current_ep = ""

    def ep_progress(ep_name: str, percent: float):
        nonlocal current_ep
        if ep_name != current_ep:
            if current_ep:
                print()
            current_ep = ep_name
        print(f"\r  {ep_name:<30}  {percent:5.1f}%", end="", flush=True)

    manager.download_and_register_eps(progress_callback=ep_progress)
    if current_ep:
        print()

    """
    Ne yapıyor? ep_progress adında küçük bir iç fonksiyon (callback) tanımlıyor. manager.download_and_register_eps fonksiyonu ise bilgisayarındaki ekran kartı (NVIDIA TensorRT, DirectML vb.) veya işlemci optimizasyon dosyalarını indirip sisteme kaydediyor.
    Neden yazdık? Yapay zekanın işlemcide mi yoksa ekran kartında mı çalışacağını belirleyen donanım kütüphanelerini (Execution Providers - EP) sisteme tanıtmak zorundayız. Yukarıdaki karmaşık görünen ep_progress fonksiyonu, tamamen terminal ekranında süslü bir yükleme çubuğu (%50.0...) görmek ve satırların birbirine karışmasını önlemek için yazılmış bir arayüz hilesidir.
    """





    # Select and load a model from the catalog
    model = manager.catalog.get_model("qwen2.5-0.5b")
    model.download(
        lambda progress: print(
            f"\rDownloading model: {progress:.2f}%",
            end="",
            flush=True,
        )
    )
    print()
    model.load()
    print("Model loaded and ready.")


    """
    Ne yapıyor? qwen2.5-0.5b isimli yapay zeka modelini hedef seçiyor. Eğer bilgisayarda yoksa internetten indiriyor (model.download). İndirme durumunu ekrana anlık basıyor. Son olarak model.load() komutuyla bu modeli bilgisayarın RAM/VRAM belleğine yüklüyor.
    Neden yazdık? Yerel yapay zekanın çalışabilmesi için bir "beyne" ihtiyacı var. Burada 500 milyon parametrelik hafif bir model seçilmiş. model.load() satırı kritik; çünkü model diskte dururken soru cevaplayamaz, matematiksel hesaplamalar için RAM'e çıkartılması şarttır.
    """



    # Get a chat client
    client = model.get_chat_client()
    
    # Create the conversation messages
    messages = [{"role": "user", "content": "What is the golden ratio?"}]


    """
    Ne yapıyor? Hafızaya yüklenen model üzerinden bir sohbet istemcisi (client) oluşturuyor. Ardından yapay zekaya göndereceğimiz mesajı bir liste ve sözlük (dictionary) yapısında hazırlıyor.
    Neden yazdık? messages yapısındaki "role": "user", bu cümleyi sistemin değil, son kullanıcının söylediğini belirtir. Yapay zeka modelleri girdi olarak bu formatı (chat template) bekler.
    """


    # Stream the response token by token
    print("Assistant: ", end="", flush=True)
    for chunk in client.complete_streaming_chat(messages):
        if not chunk.choices:
            continue
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    print()

    """
    Ne yapıyor? complete_streaming_chat fonksiyonunu çağırarak yapay zekadan cevabı üretmesini istiyor. for chunk in ... döngüsü, yapay zekanın ürettiği her bir kelime parçasını (token) anlık olarak yakalıyor ve print(..., end="", flush=True) ile kelime kelime ekrana yazdırıyor.
    Neden yazdık? Eğer streaming kullanmasaydık, yapay zeka bütün cevabı arka planda bitirene kadar (belki 10-15 saniye) ekranda hiçbir şey görmezdik ve donduğunu sanırdık. Bu döngü sayesinde ChatGPT'deki gibi akan bir yazı deneyimi elde ediyoruz.
    """




    # Clean up
    model.unload()
    print("Model unloaded.")


    """
    Ne yapıyor? İşimiz bittiğinde model.unload() diyerek RAM'e yüklediğimiz devasa yapay zeka modelini bellekten siliyor ve bilgisayarı rahatlatıyor.
    Neden yazdık? Yerel yapay zeka modelleri RAM'i çok fazla işgal eder. Eğer işimiz bittiğinde temizlemezsek, bilgisayardaki diğer programlar (örneğin tarayıcın veya oyunlar) yavaşlayabilir.
    """


if __name__ == "__main__":
    main()

