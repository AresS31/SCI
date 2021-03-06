.class Landroid/support/v4/media/MediaDescriptionCompatApi21;
.super Ljava/lang/Object;
.source "MediaDescriptionCompatApi21.java"


# annotations
.annotation build Landroid/support/annotation/RequiresApi;
    value = 0x15
.end annotation

.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Landroid/support/v4/media/MediaDescriptionCompatApi21$Builder;
    }
.end annotation


# direct methods
.method constructor <init>()V
    .registers 1

    .prologue
    .line 26
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 64
    return-void
.end method

.method public static fromParcel(Landroid/os/Parcel;)Ljava/lang/Object;
    .registers 2
    .param p0, "in"    # Landroid/os/Parcel;

    .prologue
    .line 61
    sget-object v0, Landroid/media/MediaDescription;->CREATOR:Landroid/os/Parcelable$Creator;

    invoke-interface {v0, p0}, Landroid/os/Parcelable$Creator;->createFromParcel(Landroid/os/Parcel;)Ljava/lang/Object;

    move-result-object v0

    return-object v0
.end method

.method public static getDescription(Ljava/lang/Object;)Ljava/lang/CharSequence;
    .registers 2
    .param p0, "descriptionObj"    # Ljava/lang/Object;

    .prologue
    .line 41
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0}, Landroid/media/MediaDescription;->getDescription()Ljava/lang/CharSequence;

    move-result-object v0

    return-object v0
.end method

.method public static getExtras(Ljava/lang/Object;)Landroid/os/Bundle;
    .registers 2
    .param p0, "descriptionObj"    # Ljava/lang/Object;

    .prologue
    .line 53
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0}, Landroid/media/MediaDescription;->getExtras()Landroid/os/Bundle;

    move-result-object v0

    return-object v0
.end method

.method public static getIconBitmap(Ljava/lang/Object;)Landroid/graphics/Bitmap;
    .registers 2
    .param p0, "descriptionObj"    # Ljava/lang/Object;

    .prologue
    .line 45
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0}, Landroid/media/MediaDescription;->getIconBitmap()Landroid/graphics/Bitmap;

    move-result-object v0

    return-object v0
.end method

.method public static getIconUri(Ljava/lang/Object;)Landroid/net/Uri;
    .registers 2
    .param p0, "descriptionObj"    # Ljava/lang/Object;

    .prologue
    .line 49
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0}, Landroid/media/MediaDescription;->getIconUri()Landroid/net/Uri;

    move-result-object v0

    return-object v0
.end method

.method public static getMediaId(Ljava/lang/Object;)Ljava/lang/String;
    .registers 2
    .param p0, "descriptionObj"    # Ljava/lang/Object;

    .prologue
    .line 29
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0}, Landroid/media/MediaDescription;->getMediaId()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static getSubtitle(Ljava/lang/Object;)Ljava/lang/CharSequence;
    .registers 2
    .param p0, "descriptionObj"    # Ljava/lang/Object;

    .prologue
    .line 37
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0}, Landroid/media/MediaDescription;->getSubtitle()Ljava/lang/CharSequence;

    move-result-object v0

    return-object v0
.end method

.method public static getTitle(Ljava/lang/Object;)Ljava/lang/CharSequence;
    .registers 2
    .param p0, "descriptionObj"    # Ljava/lang/Object;

    .prologue
    .line 33
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0}, Landroid/media/MediaDescription;->getTitle()Ljava/lang/CharSequence;

    move-result-object v0

    return-object v0
.end method

.method public static writeToParcel(Ljava/lang/Object;Landroid/os/Parcel;I)V
    .registers 3
    .param p0, "descriptionObj"    # Ljava/lang/Object;
    .param p1, "dest"    # Landroid/os/Parcel;
    .param p2, "flags"    # I

    .prologue
    .line 57
    check-cast p0, Landroid/media/MediaDescription;

    .end local p0    # "descriptionObj":Ljava/lang/Object;
    invoke-virtual {p0, p1, p2}, Landroid/media/MediaDescription;->writeToParcel(Landroid/os/Parcel;I)V

    .line 58
    return-void
.end method
